import argparse
import sys
import PySimpleGUI as sg
from tkinter import *
from PIL import Image, ImageDraw
import io

from ._config_file import ConfigFile
from ._editor import open_editor
from .packages import WebvizConfig, WebvizCoreComponents, WebvizSubsurface, WebvizSubsurfaceComponents
from ._cache import Cache

def run() -> bool:
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
            if not webviz_subsurface_components.is_linked_to("@webviz/core-components", str(webviz_core_components.path)):
                webviz_subsurface_components.link_to_core_components()
        else:
            if webviz_subsurface_components.is_linked_to("@webviz/core-components"):
                webviz_subsurface_components.unlink_from_core_components()
                webviz_subsurface_components.install()


        webviz_subsurface_components.build()
        return True
    except:
        return False

def open_config_editor():
    config_file = ConfigFile()
    open_editor(config_file.get_path())

def start_webviz_dev_sync(args: argparse.Namespace) -> None:

    if args.gui:
        win = sg.Window("Webviz Dev Syncer")

        def create_image_finished():
            image = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
            dc = ImageDraw.Draw(image)
            dc.ellipse((0, 0, 32, 32), fill="green", outline="green")
            return image

        def create_image_busy():
            image = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
            dc = ImageDraw.Draw(image)
            dc.ellipse((0, 0, 32, 32), fill="yellow", outline="yellow")
            return image

        def create_image_failed():
            image = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
            dc = ImageDraw.Draw(image)
            dc.ellipse((0, 0, 32, 32), fill="red", outline="red")
            return image

        menu = ["BLANK", ["&Start", "---", "&Edit Config", "---", "E&xit"]]

        img_byte_array = io.BytesIO()
        create_image_finished().save(img_byte_array, format="PNG")
        tray = sg.SystemTray(menu=menu, data_base64=img_byte_array.getvalue())
                
        while True:
            menu_item = tray.read()
            print(menu_item)
            if menu_item == "Exit":
                break
            elif menu_item == "Start":
                img_byte_array = io.BytesIO()
                create_image_busy().save(img_byte_array, format="PNG")
                tray.update(data_base64=img_byte_array.getvalue())
                if run():
                    img_byte_array = io.BytesIO()
                    create_image_finished().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())
                else:
                    img_byte_array = io.BytesIO()
                    create_image_failed().save(img_byte_array, format="PNG")
                    tray.update(data_base64=img_byte_array.getvalue())

    else:
        run()


def open_config(args: argparse.Namespace) -> None:
    open_config_editor()
