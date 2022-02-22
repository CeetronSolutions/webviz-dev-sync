import sys
from .._exec import exec

from .._package_manager import PackageManager

from .._utils import print_progress_bar

class WebvizConfig(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-config")

    def execute_package_specific_installation_routine(self) -> None:
        print_progress_bar(0, 3, prefix="Installing npm dependencies:")
        exec(["npm", "ci", "--ignore-scripts"], cwd=self._path, shell=True)
        print_progress_bar(1, 3, prefix="Running npm postinstall:")
        exec(["npm", "run", "postinstall"], cwd=self._path, shell=True)
        print_progress_bar(2, 3, prefix="Installing Python package:")
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
        print_progress_bar(3, 3, prefix="Complete")

    def get_build_timestamp(self) -> float:
        return 0
