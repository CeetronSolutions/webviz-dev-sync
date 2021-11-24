from typing import Tuple
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor

from ._config_file import ConfigFile
from ._editor import open_editor
from .packages import (
    WebvizConfig,
    WebvizCoreComponents,
    WebvizSubsurface,
    WebvizSubsurfaceComponents,
)
from ._cache import Cache


def run() -> Tuple[bool, str]:
    try:
        cache = Cache()
        config_file = ConfigFile()
        if config_file.get_last_modified_ms() > cache.get_config_modified_timestamp():
            if not config_file.check_validity():
                sys.exit()
            cache.store_config_modified_timestamp()

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
        return (True, "")
    except Exception as e:
        return (False, str(e))


def open_config_editor() -> None:
    config_file = ConfigFile()
    open_editor(config_file.get_path())


def start_webviz_dev_sync(args: argparse.Namespace) -> None:

    if args.gui:
        import PySimpleGUI as sg
        from PIL import Image, ImageDraw
        import io

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
            dc.rectangle((0, 0, 32, 32), fill="red", outline="red")
            return image

        menu = ["BLANK", ["&Start", "---", "&Edit Config", "---", "E&xit"]]

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
                elif menu_item == "Start":
                    img_byte_array = io.BytesIO()
                    create_image_busy().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    future = pool.submit(run)
                    tray.notify(
                        "Started syncing",
                        "Started syncing of all your webviz packages.",
                        icon="pending.png",
                    )
            elif future.done():
                if future.result()[0]:
                    img_byte_array = io.BytesIO()
                    create_image_finished().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    tray.notify(
                        "Syncing successful",
                        "All packages synced, ready to code :-)",
                    )
                else:
                    img_byte_array = io.BytesIO()
                    create_image_failed().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                    tray.notify(
                        "Syncing failed",
                        "Make sure your config file is valid. Exception: \n"
                        + future.result()[1],
                        icon="error.png",
                    )

                future = None

    else:
        run()


def open_config(args: argparse.Namespace) -> None:
    open_config_editor()
