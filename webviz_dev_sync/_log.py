from typing import List
from pathlib import Path
import sys

from ._user_data_dir import user_data_dir

def log_message(msg: str) -> None:

    with open(Path.joinpath(user_data_dir(), ".build.log"), "a") as log:
        print(msg)
        log.write(msg + "\n")