import subprocess
import sys

from .._package_manager import PackageManager


class WebvizSubsurfaceComponents(PackageManager):
    def __init__(self):
        PackageManager.__init__(self, "webviz-subsurface-components")

    def install(self) -> None:
        subprocess.check_call(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path, shell=True)
        subprocess.check_call(
            ["npm", "run", "setup-deckgl-types", "--prefix", "./react"], cwd=self._path, shell=True)
        subprocess.check_call(
            ["npm", "run", "copy-package-json", "--prefix", "./react"], cwd=self._path, shell=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path, shell=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path, shell=True)
        subprocess.check_call(
            ["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
