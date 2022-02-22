import sys
import os
from .._exec import exec

from .._package_manager import PackageManager
from .._utils import print_progress_bar

class WebvizSubsurfaceComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-subsurface-components")

    def execute_package_specific_installation_routine(self) -> None:
        print_progress_bar(0, 7, prefix="Installing npm dependencies:")
        exec(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"], cwd=self._path, shell=True
        )
        print_progress_bar(1, 7, prefix="Setting up 'deckgl' types:")
        exec(
            ["npm", "run", "setup-deckgl-types", "--prefix", "./react"], cwd=self._path, shell=True
        )
        print_progress_bar(2, 7, prefix="Copying 'package.json' file:")
        exec(
            ["npm", "run", "copy-package-json", "--prefix", "./react"], cwd=self._path, shell=True
        )
        print_progress_bar(3, 7, prefix="Installing Python dependencies:")
        exec(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"], cwd=self._path, shell=True
        )
        print_progress_bar(4, 7, prefix="Installing Dash dependencies:")
        exec(
            [sys.executable, "-m", "pip", "install", "dash[dev]"], cwd=self._path, shell=True
        )
        print_progress_bar(5, 7, prefix="Building npm package:")
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        print_progress_bar(6, 7, prefix="Installing Python package:")
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
        print_progress_bar(7, 7, prefix="Complete")

    def execute_package_specific_build_routine(self) -> None:
        print_progress_bar(0, 2, prefix="Building npm package:")
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        print_progress_bar(1, 2, prefix="Installing Python package:")
        exec([sys.executable, "-m", "pip", "install", "-e", "."], cwd=self._path, shell=True)
        print_progress_bar(2, 2, prefix="Complete")

    def get_build_timestamp(self) -> float:
        return os.path.getmtime(
            os.path.join(self._path, "webviz_subsurface_components")
        )

    def link_to_core_components(self) -> bool:
        try:
            exec(
                ["npm", "link", "@webviz/core-components"],
                cwd=os.path.join(self._path, "react"), shell=True,
            )
            exec(
                ["npm", "run", "setup-deckgl-types", "--prefix", "./react"],
                cwd=self._path,
                shell=True,
            )
            return True
        except:
            return False

    def unlink_from_core_components(self) -> bool:
        try:
            exec(
                ["npm", "unlink", "@webviz/core-components", "--prefix", "react"],
                cwd=os.path.join(self._path, "react"),
                shell=True,
            )
            return True
        except:
            return False
