import sys
import os
from subprocess import check_call

from .._package_manager import PackageManager

from .._exec import exec
from .._utils import print_progress_bar

class WebvizCoreComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-core-components")

    def execute_package_specific_installation_routine(self) -> None:
        print_progress_bar(0, 5, prefix="Installing npm dependencies:")
        exec(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path, shell=True
        )
        print_progress_bar(1, 5, prefix="Building npm package:")
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        print_progress_bar(2, 5, prefix="Installing Python dependencies:")
        exec(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path, shell=True
        )
        print_progress_bar(3, 5, prefix="Installing Dash dependencies:")
        exec(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path, shell=True
        )
        print_progress_bar(4, 5, prefix="Installing Python package:")
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
        print_progress_bar(5, 5, prefix="Complete")

    def execute_package_specific_build_routine(self) -> None:
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)

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
