import sys
from subprocess import check_call

from .._package_manager import PackageManager


class WebvizSubsurface(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-subsurface")

    def execute_package_specific_installation_routine(self) -> None:
        check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return 0
