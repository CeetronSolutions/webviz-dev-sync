import argparse
import sys
from git import Repo

from ._config_file import ConfigFile
from ._editor import open_editor
from .packages import WebvizConfig, WebvizCoreComponents, WebvizSubsurface, WebvizSubsurfaceComponents
from ._cache import Cache


def start_webviz_dev_sync(args: argparse.Namespace) -> None:
    cache = Cache()
    config_file = ConfigFile()
    if config_file.get_last_modified_ms() > cache.get_config_modified_timestamp():
        cache.store_config_modified_timestamp()
        if not config_file.check_validity():
            sys.exit()

    webviz_core_components = WebvizCoreComponents()
    webviz_subsurface_components = WebvizSubsurfaceComponents()
    webviz_config = WebvizConfig()
    webviz_subsurface = WebvizSubsurface()

    webviz_config.install()
    webviz_subsurface.install()
    webviz_core_components.install()
    webviz_subsurface_components.install()

    webviz_core_components.build()
    webviz_subsurface_components.build()

    if webviz_core_components.link():
        webviz_subsurface_components.link_to_core_components()    


def open_config(args: argparse.Namespace) -> None:
    config_file = ConfigFile()
    open_editor(config_file.get_path())


def print_config(args: argparse.Namespace) -> None:
    pass
