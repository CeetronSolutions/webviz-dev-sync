import sys
import os
from subprocess import check_call

from .._package_manager import PackageManager


class WebvizCoreComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-core-components")

    def execute_package_specific_installation_routine(self) -> None:
        check_call(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path
        )
        check_call(["npm", "run", "build", "--prefix", "react"], cwd=self._path)
        check_call(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path
        )
        check_call(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path
        )
        check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def execute_package_specific_build_routine(self) -> None:
        check_call(["npm", "run", "build", "--prefix", "react"], cwd=self._path)
        check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return os.path.getmtime(os.path.join(self._path, "webviz_core_components"))

    def link(self) -> bool:
        try:
            check_call(["npm", "link"], cwd=os.path.join(self._path, "react"))
            return True
        except:
            return False

    def unlink(self) -> bool:
        try:
            check_call(["npm", "unlink"], cwd=os.path.join(self._path, "react"))
            return True
        except:
            return False
