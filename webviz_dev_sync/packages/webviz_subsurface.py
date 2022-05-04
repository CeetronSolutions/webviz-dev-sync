import sys

from progress.bar import ChargingBar

from .._package_manager import PackageManager

from .._exec import exec


class WebvizSubsurface(PackageManager):
    def __init__(self) -> None:
        PackageManager.__init__(self, "webviz-subsurface")

    def execute_package_specific_installation_routine(self) -> None:
        bar = ChargingBar("Installing Python package:", max=1)
        bar.update()
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
