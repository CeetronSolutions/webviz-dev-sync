import argparse
import sys
from git import Repo

from .config_file import ConfigFile
from .editor import open_editor
from ._package_manager import PackageManager
from ._github_manager import GithubManager


def start_webviz_dev_sync(args: argparse.Namespace) -> None:
    config_file = ConfigFile()
    if not config_file.check_validity():
        sys.exit()

    manager = PackageManager("webviz-core-components")
    github = GithubManager("equinor/webviz-core-components")
    print(github.get_all_branches())


def open_config(args: argparse.Namespace) -> None:
    config_file = ConfigFile()
    open_editor(config_file.get_path())


def print_config(args: argparse.Namespace) -> None:
    pass
