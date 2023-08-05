"""
Periodically update bundled versions.
"""


from __future__ import annotations

import json
import logging
import os
import ssl
import sys
from datetime import datetime, timedelta
from itertools import groupby
from pathlib import Path
from shutil import copy2
from subprocess import PIPE, Popen
from textwrap import dedent
from threading import Thread
from urllib.error import URLError
from urllib.request import urlopen

from virtualenv.app_data import AppDataDiskFolder
from virtualenv.util.subprocess import CREATE_NO_WINDOW

from ..wheels.embed import BUNDLE_SUPPORT
from ..wheels.util import Wheel

GRACE_PERIOD_CI = timedelta(hours=1)  # prevent version switch in the middle of a CI run
GRACE_PERIOD_MINOR = timedelta(days=28)
UPDATE_PERIOD = timedelta(days=14)
UPDATE_ABORTED_DELAY = timedelta(hours=1)


def periodic_update(distribution, of_version, for_py_version, wheel, search_dirs, app_data, do_periodic_update, env):
    if do_periodic_update:
        handle_auto_update(distribution, for_py_version, wheel, search_dirs, app_data, env)

    now = datetime.now()

    def _update_wheel(ver):
        updated_wheel = Wheel(app_data.house / ver.filename)
        logging.debug("using %supdated wheel %s", "periodically " if updated_wheel else "", updated_wheel)
        return updated_wheel

    u_log = UpdateLog.from_app_data(app_data, distribution, for_py_version)
    if of_version is None:
        for _, group in groupby(u_log.versions, key=lambda v: v.wheel.version_tuple[0:2]):
            # use only latest patch version per minor, earlier assumed to be buggy
            all_patches = list(group)
            ignore_grace_period_minor = any(version for version in all_patches if version.use(now))
            for version in all_patches:
                if wheel is not None and Path(version.filename).name == wheel.name:
                    return wheel
                if version.use(now, ignore_grace_period_minor):
                    return _update_wheel(version)
    else:
        for version in u_log.versions:
            if version.wheel.version == of_version:
                return _update_wheel(version)

    return wheel


def handle_auto_update(distribution, for_py_version, wheel, search_dirs, app_data, env):
    embed_update_log = app_data.embed_update_log(distribution, for_py_version)
    u_log = UpdateLog.from_dict(embed_update_log.read())
    if u_log.needs_update:
        u_log.periodic = True
        u_log.started = datetime.now()
        embed_update_log.write(u_log.to_dict())
        trigger_update(distribution, for_py_version, wheel, search_dirs, app_data, periodic=True, env=env)


def add_wheel_to_update_log(wheel, for_py_version, app_data):
    embed_update_log = app_data.embed_update_log(wheel.distribution, for_py_version)
    logging.debug("adding %s information to %s", wheel.name, embed_update_log.file)
    u_log = UpdateLog.from_dict(embed_update_log.read())
    if any(version.filename == wheel.name for version in u_log.versions):
        logging.warning("%s already present in %s", wheel.name, embed_update_log.file)
        return
    # we don't need a release date for sources other than "periodic"
    version = NewVersion(wheel.name, datetime.now(), None, "download")
    u_log.versions.append(version)  # always write at the end for proper updates
    embed_update_log.write(u_log.to_dict())


DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


def dump_datetime(value):
    return None if value is None else value.strftime(DATETIME_FMT)


def load_datetime(value):
    return None if value is None else datetime.strptime(value, DATETIME_FMT)


class NewVersion:
    def __init__(self, filename, found_date, release_date, source):
        self.filename = filename
        self.found_date = found_date
        self.release_date = release_date
        self.source = source

    @classmethod
    def from_dict(cls, dictionary):
        return cls(
            filename=dictionary["filename"],
            found_date=load_datetime(dictionary["found_date"]),
            release_date=load_datetime(dictionary["release_date"]),
            source=dictionary["source"],
        )

    def to_dict(self):
        return {
            "filename": self.filename,
            "release_date": dump_datetime(self.release_date),
            "found_date": dump_datetime(self.found_date),
            "source": self.source,
        }

    def use(self, now, ignore_grace_period_minor=False, ignore_grace_period_ci=False):
        if self.source == "manual":
            return True
        elif self.source == "periodic":
            if self.found_date < now - GRACE_PERIOD_CI or ignore_grace_period_ci:
                if not ignore_grace_period_minor:
                    compare_from = self.release_date or self.found_date
                    return now - compare_from >= GRACE_PERIOD_MINOR
                return True
        return False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(filename={self.filename}), found_date={self.found_date}, "
            f"release_date={self.release_date}, source={self.source})"
        )

    def __eq__(self, other):
        return type(self) == type(other) and all(
            getattr(self, k) == getattr(other, k) for k in ["filename", "release_date", "found_date", "source"]
        )

    def __ne__(self, other):
        return not (self == other)

    @property
    def wheel(self):
        return Wheel(Path(self.filename))


class UpdateLog:
    def __init__(self, started, completed, versions, periodic):
        self.started = started
        self.completed = completed
        self.versions = versions
        self.periodic = periodic

    @classmethod
    def from_dict(cls, dictionary):
        if dictionary is None:
            dictionary = {}
        return cls(
            load_datetime(dictionary.get("started")),
            load_datetime(dictionary.get("completed")),
            [NewVersion.from_dict(v) for v in dictionary.get("versions", [])],
            dictionary.get("periodic"),
        )

    @classmethod
    def from_app_data(cls, app_data, distribution, for_py_version):
        raw_json = app_data.embed_update_log(distribution, for_py_version).read()
        return cls.from_dict(raw_json)

    def to_dict(self):
        return {
            "started": dump_datetime(self.started),
            "completed": dump_datetime(self.completed),
            "periodic": self.periodic,
            "versions": [r.to_dict() for r in self.versions],
        }

    @property
    def needs_update(self):
        now = datetime.now()
        if self.completed is None:  # never completed
            return self._check_start(now)
        else:
            if now - self.completed <= UPDATE_PERIOD:
                return False
            return self._check_start(now)

    def _check_start(self, now):
        return self.started is None or now - self.started > UPDATE_ABORTED_DELAY


def trigger_update(distribution, for_py_version, wheel, search_dirs, app_data, env, periodic):
    wheel_path = None if wheel is None else str(wheel.path)
    cmd = [
        sys.executable,
        "-c",
        dedent(
            """
        from virtualenv.report import setup_report, MAX_LEVEL
        from virtualenv.seed.wheels.periodic_update import do_update
        setup_report(MAX_LEVEL, show_pid=True)
        do_update({!r}, {!r}, {!r}, {!r}, {!r}, {!r})
        """,
        )
        .strip()
        .format(distribution, for_py_version, wheel_path, str(app_data), [str(p) for p in search_dirs], periodic),
    ]
    debug = env.get("_VIRTUALENV_PERIODIC_UPDATE_INLINE") == "1"
    pipe = None if debug else PIPE
    kwargs = {"stdout": pipe, "stderr": pipe}
    if not debug and sys.platform == "win32":
        kwargs["creationflags"] = CREATE_NO_WINDOW
    process = Popen(cmd, **kwargs)
    logging.info(
        "triggered periodic upgrade of %s%s (for python %s) via background process having PID %d",
        distribution,
        "" if wheel is None else f"=={wheel.version}",
        for_py_version,
        process.pid,
    )
    if debug:
        process.communicate()  # on purpose not called to make it a background process


def do_update(distribution, for_py_version, embed_filename, app_data, search_dirs, periodic):
    versions = None
    try:
        versions = _run_do_update(app_data, distribution, embed_filename, for_py_version, periodic, search_dirs)
    finally:
        logging.debug("done %s %s with %s", distribution, for_py_version, versions)
    return versions


def _run_do_update(app_data, distribution, embed_filename, for_py_version, periodic, search_dirs):
    from virtualenv.seed.wheels import acquire

    wheel_filename = None if embed_filename is None else Path(embed_filename)
    embed_version = None if wheel_filename is None else Wheel(wheel_filename).version_tuple
    app_data = AppDataDiskFolder(app_data) if isinstance(app_data, str) else app_data
    search_dirs = [Path(p) if isinstance(p, str) else p for p in search_dirs]
    wheelhouse = app_data.house
    embed_update_log = app_data.embed_update_log(distribution, for_py_version)
    u_log = UpdateLog.from_dict(embed_update_log.read())
    now = datetime.now()

    update_versions, other_versions = [], []
    for version in u_log.versions:
        if version.source in {"periodic", "manual"}:
            update_versions.append(version)
        else:
            other_versions.append(version)

    if periodic:
        source = "periodic"
    else:
        source = "manual"
        # mark the most recent one as source "manual"
        if update_versions:
            update_versions[0].source = source

    if wheel_filename is not None:
        dest = wheelhouse / wheel_filename.name
        if not dest.exists():
            copy2(str(wheel_filename), str(wheelhouse))
    last, last_version, versions, filenames = None, None, [], set()
    while last is None or not last.use(now, ignore_grace_period_ci=True):
        download_time = datetime.now()
        dest = acquire.download_wheel(
            distribution=distribution,
            version_spec=None if last_version is None else f"<{last_version}",
            for_py_version=for_py_version,
            search_dirs=search_dirs,
            app_data=app_data,
            to_folder=wheelhouse,
            env=os.environ,
        )
        if dest is None or (update_versions and update_versions[0].filename == dest.name):
            break
        release_date = release_date_for_wheel_path(dest.path)
        last = NewVersion(filename=dest.path.name, release_date=release_date, found_date=download_time, source=source)
        logging.info("detected %s in %s", last, datetime.now() - download_time)
        versions.append(last)
        filenames.add(last.filename)
        last_wheel = last.wheel
        last_version = last_wheel.version
        if embed_version is not None:
            if embed_version >= last_wheel.version_tuple:  # stop download if we reach the embed version
                break
    u_log.periodic = periodic
    if not u_log.periodic:
        u_log.started = now
    # update other_versions by removing version we just found
    other_versions = [version for version in other_versions if version.filename not in filenames]
    u_log.versions = versions + update_versions + other_versions
    u_log.completed = datetime.now()
    embed_update_log.write(u_log.to_dict())
    return versions


def release_date_for_wheel_path(dest):
    wheel = Wheel(dest)
    # the most accurate is to ask PyPi - e.g. https://pypi.org/pypi/pip/json,
    # see https://warehouse.pypa.io/api-reference/json/ for more details
    content = _pypi_get_distribution_info_cached(wheel.distribution)
    if content is not None:
        try:
            upload_time = content["releases"][wheel.version][0]["upload_time"]
            return datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S")
        except Exception as exception:
            logging.error("could not load release date %s because %r", content, exception)
    return None


def _request_context():
    yield None
    # fallback to non verified HTTPS (the information we request is not sensitive, so fallback)
    yield ssl._create_unverified_context()


_PYPI_CACHE = {}


def _pypi_get_distribution_info_cached(distribution):
    if distribution not in _PYPI_CACHE:
        _PYPI_CACHE[distribution] = _pypi_get_distribution_info(distribution)
    return _PYPI_CACHE[distribution]


def _pypi_get_distribution_info(distribution):
    content, url = None, f"https://pypi.org/pypi/{distribution}/json"
    try:
        for context in _request_context():
            try:
                with urlopen(url, context=context) as file_handler:
                    content = json.load(file_handler)
                break
            except URLError as exception:
                logging.error("failed to access %s because %r", url, exception)
    except Exception as exception:
        logging.error("failed to access %s because %r", url, exception)
    return content


def manual_upgrade(app_data, env):
    threads = []

    for for_py_version, distribution_to_package in BUNDLE_SUPPORT.items():
        # load extra search dir for the given for_py
        for distribution in distribution_to_package.keys():
            thread = Thread(target=_run_manual_upgrade, args=(app_data, distribution, for_py_version, env))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()


def _run_manual_upgrade(app_data, distribution, for_py_version, env):
    start = datetime.now()
    from .bundle import from_bundle

    current = from_bundle(
        distribution=distribution,
        version=None,
        for_py_version=for_py_version,
        search_dirs=[],
        app_data=app_data,
        do_periodic_update=False,
        env=env,
    )
    logging.warning(
        "upgrade %s for python %s with current %s",
        distribution,
        for_py_version,
        "" if current is None else current.name,
    )
    versions = do_update(
        distribution=distribution,
        for_py_version=for_py_version,
        embed_filename=current.path,
        app_data=app_data,
        search_dirs=[],
        periodic=False,
    )

    args = [
        distribution,
        for_py_version,
        datetime.now() - start,
    ]
    if versions:
        args.append("\n".join(f"\t{v}" for v in versions))
    ver_update = "new entries found:\n%s" if versions else "no new versions found"
    logging.warning(f"upgraded %s for python %s in %s {ver_update}", *args)


__all__ = [
    "add_wheel_to_update_log",
    "periodic_update",
    "do_update",
    "manual_upgrade",
    "NewVersion",
    "UpdateLog",
    "load_datetime",
    "dump_datetime",
    "trigger_update",
    "release_date_for_wheel_path",
]
