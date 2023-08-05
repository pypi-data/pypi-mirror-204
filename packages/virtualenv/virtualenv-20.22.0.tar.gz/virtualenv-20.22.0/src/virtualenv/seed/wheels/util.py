from __future__ import annotations

from operator import attrgetter
from zipfile import ZipFile


class Wheel:
    def __init__(self, path):
        # https://www.python.org/dev/peps/pep-0427/#file-name-convention
        # The wheel filename is {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
        self.path = path
        self._parts = path.stem.split("-")

    @classmethod
    def from_path(cls, path):
        if path is not None and path.suffix == ".whl" and len(path.stem.split("-")) >= 5:
            return cls(path)
        return None

    @property
    def distribution(self):
        return self._parts[0]

    @property
    def version(self):
        return self._parts[1]

    @property
    def version_tuple(self):
        return self.as_version_tuple(self.version)

    @staticmethod
    def as_version_tuple(version):
        result = []
        for part in version.split(".")[0:3]:
            try:
                result.append(int(part))
            except ValueError:
                break
        if not result:
            raise ValueError(version)
        return tuple(result)

    @property
    def name(self):
        return self.path.name

    def support_py(self, py_version):
        name = f"{'-'.join(self.path.stem.split('-')[0:2])}.dist-info/METADATA"
        with ZipFile(str(self.path), "r") as zip_file:
            metadata = zip_file.read(name).decode("utf-8")
        marker = "Requires-Python:"
        requires = next((i[len(marker) :] for i in metadata.splitlines() if i.startswith(marker)), None)
        if requires is None:  # if it does not specify a python requires the assumption is compatible
            return True
        py_version_int = tuple(int(i) for i in py_version.split("."))
        for require in (i.strip() for i in requires.split(",")):
            # https://www.python.org/dev/peps/pep-0345/#version-specifiers
            for operator, check in [
                ("!=", lambda v: py_version_int != v),
                ("==", lambda v: py_version_int == v),
                ("<=", lambda v: py_version_int <= v),
                (">=", lambda v: py_version_int >= v),
                ("<", lambda v: py_version_int < v),
                (">", lambda v: py_version_int > v),
            ]:
                if require.startswith(operator):
                    ver_str = require[len(operator) :].strip()
                    version = tuple((int(i) if i != "*" else None) for i in ver_str.split("."))[0:2]
                    if not check(version):
                        return False
                    break
        return True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path})"

    def __str__(self):
        return str(self.path)


def discover_wheels(from_folder, distribution, version, for_py_version):
    wheels = []
    for filename in from_folder.iterdir():
        wheel = Wheel.from_path(filename)
        if wheel and wheel.distribution == distribution:
            if version is None or wheel.version == version:
                if wheel.support_py(for_py_version):
                    wheels.append(wheel)
    return sorted(wheels, key=attrgetter("version_tuple", "distribution"), reverse=True)


class Version:
    #: the version bundled with virtualenv
    bundle = "bundle"
    embed = "embed"
    #: custom version handlers
    non_version = (bundle, embed)

    @staticmethod
    def of_version(value):
        return None if value in Version.non_version else value

    @staticmethod
    def as_pip_req(distribution, version):
        return f"{distribution}{Version.as_version_spec(version)}"

    @staticmethod
    def as_version_spec(version):
        of_version = Version.of_version(version)
        return "" if of_version is None else f"=={of_version}"


__all__ = [
    "discover_wheels",
    "Version",
    "Wheel",
]
