try:
    # Python 3.8+
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

from .webviz_dev_sync import start_webviz_dev_sync

try:
    __version__ = version("webviz-dev-sync")
except PackageNotFoundError:
    # package is not installed
    pass