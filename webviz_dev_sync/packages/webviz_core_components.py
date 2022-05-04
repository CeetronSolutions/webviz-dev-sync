import sys
import os
from subprocess import check_call

from progress.bar import ChargingBar

from .._package_manager import PackageManager

from .._exec import exec


class WebvizCoreComponents(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-core-components")

    def execute_package_specific_installation_routine(self) -> None:
        bar = ChargingBar("Installing npm dependencies:", max=5)
        bar.update()
        exec(
            ["npm", "ci", "--ignore-scripts", "--prefix", "./react"],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Building npm package:"
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        bar.next()
        bar.message = "Installing Python dependencies:"
        exec(
            [sys.executable, "-m", "pip", "install", ".[dependencies]"],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Installing Dash dependencies:"
        exec(
            [sys.executable, "-m", "pip", "install", "dash[dev]"],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Installing Python package:"
        exec(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Complete:"
        bar.finish()

    def execute_package_specific_build_routine(self) -> None:
        bar = ChargingBar("Building npm package:", max=2)
        bar.update()
        exec(["npm", "run", "build", "--prefix", "react"], cwd=self._path, shell=True)
        bar.next()
        bar.message = "Installing Python package:"
        exec(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Complete:"
        bar.finish()

    def get_build_timestamp(self) -> float:
        return os.path.getmtime(os.path.join(self._path, "webviz_core_components"))

    def link(self) -> bool:
        try:
            exec(["npm", "link"], cwd=self._path.joinpath("react"), shell=True)
            return True
        except:
            return False

    def unlink(self) -> bool:
        try:
            exec(["npm", "unlink"], cwd=self._path.joinpath("react"), shell=True)
            return True
        except:
            return False
