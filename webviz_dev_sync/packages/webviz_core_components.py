import sys
import os
from subprocess import check_call

from .._package_manager import PackageManager

from .._exec import exec


class WebvizCoreComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-core-components")

    def execute_package_specific_installation_routine(self) -> None:
        exec(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path, shell=True
        )
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        exec(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path
        )
        exec(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path
        )
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def execute_package_specific_build_routine(self) -> None:
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return os.path.getmtime(os.path.join(self._path, "webviz_core_components"))

    def link(self) -> bool:
        try:
            exec(["npm", "link"], cwd=os.path.join(self._path, "react"), shell=True)
            return True
        except:
            return False

    def unlink(self) -> bool:
        try:
            exec(["npm", "unlink"], cwd=os.path.join(self._path, "react"), shell=True)
            return True
        except:
            return False
