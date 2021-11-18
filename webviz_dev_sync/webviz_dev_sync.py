import argparse

from .config_file import ConfigFile


def start_webviz_dev_sync(args: argparse.Namespace) -> None:
    config_file = ConfigFile()
    webviz_core_components = config_file.get_package("webviz-core-components")
    print(webviz_core_components)


def open_config(args: argparse.Namespace) -> None:


def print_config(args: argparse.Namespace) -> None:
