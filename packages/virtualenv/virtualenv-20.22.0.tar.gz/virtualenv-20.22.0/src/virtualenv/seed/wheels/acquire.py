"""Bootstrap"""

from __future__ import annotations

import logging
import sys
from operator import eq, lt
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen

from .bundle import from_bundle
from .periodic_update import add_wheel_to_update_log
from .util import Version, Wheel, discover_wheels


def get_wheel(distribution, version, for_py_version, search_dirs, download, app_data, do_periodic_update, env):
    """
    Get a wheel with the given distribution-version-for_py_version trio, by using the extra search dir + download
    """
    # not all wheels are compatible with all python versions, so we need to py version qualify it
    wheel = None

    if not download or version != Version.bundle:
        # 1. acquire from bundle
        wheel = from_bundle(distribution, version, for_py_version, search_dirs, app_data, do_periodic_update, env)

    if download and wheel is None and version != Version.embed:
        # 2. download from the internet
        wheel = download_wheel(
            distribution=distribution,
            version_spec=Version.as_version_spec(version),
            for_py_version=for_py_version,
            search_dirs=search_dirs,
            app_data=app_data,
            to_folder=app_data.house,
            env=env,
        )
        if wheel is not None and app_data.can_update:
            add_wheel_to_update_log(wheel, for_py_version, app_data)

    return wheel


def download_wheel(distribution, version_spec, for_py_version, search_dirs, app_data, to_folder, env):
    to_download = f"{distribution}{version_spec or ''}"
    logging.debug("download wheel %s %s to %s", to_download, for_py_version, to_folder)
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--progress-bar",
        "off",
        "--disable-pip-version-check",
        "--only-binary=:all:",
        "--no-deps",
        "--python-version",
        for_py_version,
        "-d",
        str(to_folder),
        to_download,
    ]
    # pip has no interface in python - must be a new sub-process
    env = pip_wheel_env_run(search_dirs, app_data, env)
    process = Popen(cmd, env=env, stdout=PIPE, stderr=PIPE, universal_newlines=True, encoding="utf-8")
    out, err = process.communicate()
    if process.returncode != 0:
        kwargs = {"output": out, "stderr": err}
        raise CalledProcessError(process.returncode, cmd, **kwargs)
    result = _find_downloaded_wheel(distribution, version_spec, for_py_version, to_folder, out)
    logging.debug("downloaded wheel %s", result.name)
    return result


def _find_downloaded_wheel(distribution, version_spec, for_py_version, to_folder, out):
    for line in out.splitlines():
        line = line.lstrip()
        for marker in ("Saved ", "File was already downloaded "):
            if line.startswith(marker):
                return Wheel(Path(line[len(marker) :]).absolute())
    # if for some reason the output does not match fallback to the latest version with that spec
    return find_compatible_in_house(distribution, version_spec, for_py_version, to_folder)


def find_compatible_in_house(distribution, version_spec, for_py_version, in_folder):
    wheels = discover_wheels(in_folder, distribution, None, for_py_version)
    start, end = 0, len(wheels)
    if version_spec is not None and version_spec != "":
        if version_spec.startswith("<"):
            from_pos, op = 1, lt
        elif version_spec.startswith("=="):
            from_pos, op = 2, eq
        else:
            raise ValueError(version_spec)
        version = Wheel.as_version_tuple(version_spec[from_pos:])
        start = next((at for at, w in enumerate(wheels) if op(w.version_tuple, version)), len(wheels))

    return None if start == end else wheels[start]


def pip_wheel_env_run(search_dirs, app_data, env):
    env = env.copy()
    env.update({"PIP_USE_WHEEL": "1", "PIP_USER": "0", "PIP_NO_INPUT": "1"})
    wheel = get_wheel(
        distribution="pip",
        version=None,
        for_py_version=f"{sys.version_info.major}.{sys.version_info.minor}",
        search_dirs=search_dirs,
        download=False,
        app_data=app_data,
        do_periodic_update=False,
        env=env,
    )
    if wheel is None:
        raise RuntimeError("could not find the embedded pip")
    env["PYTHONPATH"] = str(wheel.path)
    return env


__all__ = [
    "get_wheel",
    "download_wheel",
    "pip_wheel_env_run",
]
