from typing import Tuple
import argparse
import sys
import os
from pathlib import Path
import shutil
from pkg_resources import get_distribution

from github import BadCredentialsException

from ._config_file import ConfigFile
from ._editor import open_editor
from .packages import (
    WebvizConfig,
    WebvizCoreComponents,
    WebvizSubsurface,
    WebvizSubsurfaceComponents,
)
from ._cache import Cache

from ._user_data_dir import user_data_dir

from ._log import log_message

from ._exec import exec

from ._package_manager import MissingPackageInConfigFile

from ._app_info import print_logo_and_version

def run() -> Tuple[bool, str]:
    print_logo_and_version()

    try:
        # Make sure directory exists
        os.makedirs(user_data_dir(), exist_ok=True)

        with open(Path.joinpath(user_data_dir(), ".build.log"), "w") as log_file:
            log_file.write("")

        cache = Cache()
        config_file = ConfigFile()
        if config_file.get_last_modified_ms() > cache.get_config_modified_timestamp():
            print("\nDetected changes to config file. Validating...")
            if not config_file.check_validity():
                sys.exit()
            cache.store_config_modified_timestamp()
            print("\u2713 Config file valid.")

        webviz_core_components = WebvizCoreComponents()
        webviz_subsurface_components = WebvizSubsurfaceComponents()
        webviz_config = WebvizConfig()
        webviz_subsurface = WebvizSubsurface()

        webviz_config.install()
        webviz_subsurface.install()

        webviz_core_components.install()
        webviz_core_components.build()

        if not webviz_core_components.is_linked():
            if not webviz_core_components.link():
                sys.exit()

        if webviz_subsurface_components.shall_be_linked():
            webviz_subsurface_components.install()
            if not webviz_subsurface_components.is_linked_to(
                "@webviz/core-components", str(webviz_core_components.path)
            ):
                webviz_subsurface_components.link_to_core_components()
        else:
            if webviz_subsurface_components.is_linked_to("@webviz/core-components"):
                webviz_subsurface_components.unlink_from_core_components()
                webviz_subsurface_components.install()

        webviz_subsurface_components.build()
        log_message(f"Sync process complete! Happy coding! =)", type="success")
        return (True, "")
    except BadCredentialsException as e:
        msg = "Your GitHub access token is either invalid or has expired. Please open the config file and provide a valid access token (use 'webviz-dev config'). Exiting now."
        log_message(msg, type="error")
        return (
            False,
            msg,
        )
    except MissingPackageInConfigFile as e:
        msg = f"Your config file is missing the package '{e}'. Please verify your config file is valid."
        log_message(msg, type="error")
        return (
            False,
            msg,
        )
    except Exception as e:
        log_message(str(e), type="error")
        print("Use 'webviz-dev log' to check the build log.")
        return (False, str(e))


def open_config_editor() -> None:
    config_file = ConfigFile()
    open_editor(config_file.get_path())


def open_build_log_editor() -> None:
    build_log_file = Path.joinpath(user_data_dir(), ".build.log")
    if not build_log_file.exists():
        print("No log file has been written yet. Are you sure you have already started a syncing process?")
        exit()

    open_editor(str(build_log_file))


def start_webviz_dev_sync(args: argparse.Namespace) -> None:

    if args.gui:
        import io
        from concurrent.futures import ProcessPoolExecutor

        import PySimpleGUI as sg
        from PIL import Image, ImageDraw

        win = sg.Window("Webviz Dev Syncer")

        def create_image_finished() -> Image:
            image = Image.new("RGB", (32, 32), (255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.rectangle((0, 0, 32, 32), fill="green", outline="green")
            return image

        def create_image_busy() -> Image:
            image = Image.new("RGB", (32, 32), (255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.rectangle((0, 0, 32, 32), fill="yellow", outline="yellow")
            return image

        def create_image_failed() -> Image:
            image = Image.new("RGB", (32, 32), (255, 255, 255))
            dc = ImageDraw.Draw(image)
            dc.rectangle((0, 0, 32, 32), fill="#D50000", outline="#D50000")
            return image

        menu = [
            "BLANK",
            ["&Start", "---", "&Edit Config", "Show &build log", "---", "E&xit"],
        ]

        img_byte_array = io.BytesIO()
        create_image_finished().save(img_byte_array, format="PNG")
        tray = sg.SystemTray(menu=menu, data_base64=img_byte_array.getvalue())

        pool = ProcessPoolExecutor(1)
        future = None

        while True:
            if not future:
                menu_item = tray.read()
                if menu_item == "Exit":
                    break
                elif menu_item == "Edit Config":
                    open_config_editor()
                elif menu_item == "Show build log":
                    open_build_log_editor()
                elif menu_item == "Start":
                    img_byte_array = io.BytesIO()
                    create_image_busy().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    future = pool.submit(run)
                    tray.notify(
                        "Started syncing",
                        "Started syncing of all your webviz packages.",
                        icon=Path.joinpath(
                            Path(__file__).parent.parent, "assets/pending.png"
                        ),
                    )
            elif future.done():
                if future.result()[0]:
                    img_byte_array = io.BytesIO()
                    create_image_finished().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    tray.notify(
                        "Syncing successful",
                        "All packages are synced. Happy coding! :-)",
                    )
                else:
                    img_byte_array = io.BytesIO()
                    create_image_failed().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    tray.notify(
                        "Syncing failed",
                        "Exception: \n" + future.result()[1],
                        icon=Path.joinpath(
                            Path(__file__).parent.parent, "assets/error.png"
                        ),
                    )

                future = None

    else:
        run()


def open_config(args: argparse.Namespace) -> None:
    open_config_editor()


def open_build_log(args: argparse.Namespace) -> None:
    open_build_log_editor()


def clean(args: argparse.Namespace) -> None:
    print_logo_and_version()
    
    repos = [
        "webviz-core-components",
        "webviz-config",
        "webviz-subsurface-components",
        "webviz-subsurface",
    ]
    repo_storage_directory = ConfigFile().get_repo_storage_directory()
    if repo_storage_directory:
        print(
            f"WARNING: This will remove all repositories that have automatically been cloned by webviz-dev in '{repo_storage_directory}':"
        )
        count = 0
        for repo in (
            repo
            for repo in repos
            if os.path.isdir(repo_storage_directory.joinpath(repo))
        ):
            print(f"- {repo_storage_directory.joinpath(repo)}")
            count += 1
        if count == 0:
            print("~\n\nNo repositories found. Aborting.")
            exit()

        answer = input(
            f"\nAre you sure you want to remove {count} repositories [Y/N]? "
        )

        if answer == "y":
            for repo in (
                repo
                for repo in repos
                if os.path.isdir(repo_storage_directory.joinpath(repo))
            ):
                print(f"\nRemoving repository '{repo}'...")
                distribution = get_distribution(repo)
                if distribution and Path(distribution.location).samefile(
                    repo_storage_directory.joinpath(repo)
                ):
                    print(f"- Uninstalling '{repo}'...")
                    try:
                        exec(
                            [
                                sys.executable,
                                "-m",
                                "pip",
                                "uninstall",
                                "-y",
                                "webviz-core-components",
                            ],
                            cwd=repo_storage_directory.joinpath(repo),
                            shell=True,
                        )
                        print("  \u2713 Sucessfully uninstalled")
                    except Exception as e:
                        print(e)
                        print("- Could not uninstall! x")
                shutil.rmtree(repo_storage_directory.joinpath(repo))
                print("\u2713 Sucessfully removed")
    else:
        print("No default repository storage directory found in config file. Exiting.")
