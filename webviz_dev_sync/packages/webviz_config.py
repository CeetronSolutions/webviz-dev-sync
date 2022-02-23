import sys

from progress.bar import ChargingBar

from .._exec import exec

from .._package_manager import PackageManager


class WebvizConfig(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-config")

    def execute_package_specific_installation_routine(self) -> None:
        bar = ChargingBar("Installing npm dependencies:", max=3)
        bar.update()
        exec(["npm", "ci", "--ignore-scripts"], cwd=self._path, shell=True)
        bar.message = "Running npm postinstall:"
        bar.next()
        exec(["npm", "run", "postinstall"], cwd=self._path, shell=True)
        bar.message = "Installing Python package:"
        bar.next()
        exec(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=self._path,
            shell=True,
        )
        bar.next()
        bar.message = "Complete"
        bar.finish()

    def get_build_timestamp(self) -> float:
        return 0
