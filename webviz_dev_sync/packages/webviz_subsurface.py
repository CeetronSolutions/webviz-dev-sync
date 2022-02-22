import sys

from .._package_manager import PackageManager

from .._exec import exec
from .._utils import print_progress_bar

class WebvizSubsurface(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-subsurface")

    def execute_package_specific_installation_routine(self) -> None:
        print_progress_bar(0, 1, prefix="Installing Python package:")
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
        print_progress_bar(1, 1, prefix="Complete")

    def get_build_timestamp(self) -> float:
        return 0
