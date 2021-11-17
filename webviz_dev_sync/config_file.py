from pathlib import Path
from yaml import safe_load, dump
from typing import Optional

from ._user_data_dir import user_data_dir


class ConfigFile:
    def __init__(self) -> None:
        self.config_file_path = Path.joinpath(user_data_dir(), "config.yaml")
        self.config_file = None
        if not self.config_file_path.exists():
            Path.mkdir(user_data_dir(), exist_ok=True)
            self.make_default_file()
        else:
            with open(self.config_file_path, encoding="utf-8", mode="r") as file:
                self.config_file = safe_load(file)

    def make_default_file(self) -> None:
        self.config_file = {
            "packages": [
                {
                    "webviz-core-components": {
                        "local": False,
                        "local_path": "",
                        "git_url": "https://github.com/equinor/webviz-core-components.git",
                    }
                },
                {
                    "webviz-subsurface-components": {
                        "local": False,
                        "local_path": "",
                        "git_url": "https://github.com/equinor/webviz-subsurface-components.git",
                    }
                },
                {
                    "webviz-config": {
                        "local": False,
                        "local_path": "",
                        "git_url": "https://github.com/equinor/webviz-config.git",
                    }
                },
                {
                    "webviz-subsurface": {
                        "local": False,
                        "local_path": "",
                        "git_url": "https://github.com/equinor/webviz-subsurface.git",
                    }
                },
            ]
        }
        with open(self.config_file_path, encoding="utf-8", mode="a") as file:
            dump(self.config_file, file)

    def get_package(self, name: str) -> Optional[dict]:
        if not self.config_file or "packages" not in self.config_file:
            return None

        package = next(
            package
            for package in self.config_file["packages"]
            if list(package.keys())[0] == name
        )

        return package
