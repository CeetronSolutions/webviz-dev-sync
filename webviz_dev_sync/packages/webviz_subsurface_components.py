import subprocess
import sys
import os

from .._package_manager import PackageManager


class WebvizSubsurfaceComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-subsurface-components")

    def execute_package_specific_installation_routine(self) -> None:
        subprocess.check_call(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path)
        subprocess.check_call(
            ["npm", "run", "setup-deckgl-types", "--prefix", "./react"], cwd=self._path)
        subprocess.check_call(
            ["npm", "run", "copy-package-json", "--prefix", "./react"], cwd=self._path)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path)
        subprocess.check_call(
            ["npm", "run", "build", "--prefix", "react"], cwd=self._path)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def execute_package_specific_build_routine(self) -> None:
        subprocess.check_call(
            ["npm", "run", "build", "--prefix", "react"], cwd=self._path)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path)

    def get_build_timestamp(self) -> float:
        return os.path.getmtime(os.path.join(self._path, "webviz_subsurface_components"))

    def link_to_core_components(self) -> bool:
        try:
            subprocess.check_call(["npm", "link", "@webviz/core-components"], cwd=os.path.join(self._path, "react"))
            subprocess.check_call(
            ["npm", "run", "setup-deckgl-types", "--prefix", "./react"], cwd=self._path)
            return True
        except:
            return False
        
    def unlink_from_core_components(self) -> bool:
        try:
            subprocess.check_call(["npm", "unlink", "@webviz/core-components", "--prefix", "react"], cwd=os.path.join(self._path, "react"))
            return True
        except:
            return False
