from typing import List
from pathlib import Path
import sys

from ._user_data_dir import user_data_dir


def log_message(msg: str, type: str = "") -> None:
    types = {"error": "\033[91m", "warning": "\033[93m", "success": "\033[92m"}
    with open(Path.joinpath(user_data_dir(), ".build.log"), "a+") as log:
        start_format = types.get(type, "")
        if start_format != "":
            start_format = "\n\n" + start_format
        end_format = "\033[0m" if format != "" else ""
        print(f"{start_format}{msg}{end_format}")
        log.write(msg + "\n")
