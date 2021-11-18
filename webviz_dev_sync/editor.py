import os
import sys
from subprocess import run
from typing import List

from .config_file import ConfigFile


def open_editor(file_path: str) -> None:
    config = ConfigFile()

    if config.get_preferred_editor():
        if try_start_editor([config.get_preferred_editor()], file_path):
            return
        print(
            f"Could not start '{config.get_preferred_editor()}'. Falling back to default."
        )

    if sys.platform.startswith("win"):
        os.startfile(file_path)
    elif sys.platform.startswith("linux"):
        run(["xdg-open", file_path])
    elif sys.platform.startswith("darwin"):
        run(["open", file_path])


def try_start_editor(editor: List[str], file_path: str) -> bool:
    editor.append(file_path)
    editor_process = run(editor)
    return editor_process.returncode == 0
