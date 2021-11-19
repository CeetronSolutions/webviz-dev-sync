import argparse
import sys
from git import Repo

from .config_file import ConfigFile
from .editor import open_editor
from .packages import WebvizConfig, WebvizCoreComponents, WebvizSubsurface, WebvizSubsurfaceComponents
from ._cache import Cache


def start_webviz_dev_sync(args: argparse.Namespace) -> None:
    cache = Cache()
    config_file = ConfigFile()
    if config_file.get_last_modified_ms() > cache.get_config_modified_date():
        cache.store_config_modified_date()
        if not config_file.check_validity():
            sys.exit()

    webviz_core_components = WebvizCoreComponents()
    webviz_subsurface_components = WebvizSubsurfaceComponents
    webviz_config = WebvizConfig()
    webviz_subsurface = WebvizSubsurface()

    webviz_config.install()
    webviz_subsurface.install()
    webviz_core_components.install()
    webviz_subsurface_components.install()


def open_config(args: argparse.Namespace) -> None:
    config_file = ConfigFile()
    open_editor(config_file.get_path())


def print_config(args: argparse.Namespace) -> None:
    pass
