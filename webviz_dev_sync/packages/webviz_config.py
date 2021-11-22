import subprocess
import sys

from .._package_manager import PackageManager


class WebvizConfig(PackageManager):
    def __init__(self):
        PackageManager.__init__(self, "webviz-config")

    def execute_package_specific_installation_routine(self) -> None:
        subprocess.check_call(
            ["npm", "ci", "--ignore-scripts"], cwd=self._path)
        subprocess.check_call(
            ["npm", "run", "postinstall"], cwd=self._path)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return 0
