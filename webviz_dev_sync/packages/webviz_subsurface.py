import subprocess
import sys

from .._package_manager import PackageManager


class WebvizSubsurface(PackageManager):
    def __init__(self):
        PackageManager.__init__(self, "webviz-subsurface")

    def install(self) -> None:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
