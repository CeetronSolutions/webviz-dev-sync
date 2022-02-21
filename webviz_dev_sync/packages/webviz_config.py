import sys
from .._exec import exec

from .._package_manager import PackageManager


class WebvizConfig(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-config")

    def execute_package_specific_installation_routine(self) -> None:
        exec(["npm", "ci", "--ignore-scripts"], cwd=self._path, shell=True)
        exec(["npm", "run", "postinstall"], cwd=self._path, shell=True)
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return 0
