import os


def open_editor(file_path: str) -> None:
    possible_editors = [
        os.environ["EDITOR"],
        "vi",
        "gedit",
        "notepad",
    ]
