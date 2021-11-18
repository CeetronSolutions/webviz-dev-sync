from pathlib import Path
import pathlib
import yaml
from typing import Optional
from jsonschema import validate, ValidationError
from getpass import getpass
import os

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
                self.config_file = yaml.safe_load(file)

    def check_validity(self) -> bool:
        if not self.config_file:
            return False

        schema_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "static/config_schema.yaml",
        )
        with open(
            schema_path,
            encoding="utf-8",
            mode="r",
        ) as schema:
            try:
                validate(self.config_file, yaml.safe_load(schema))
                return True
            except ValidationError as e:
                print(
                    "Config file is invalid. Please fix the following errors: \n"
                    + str(e)
                )

        return False

    def make_default_file(self) -> None:
        github_token = getpass(
            "Please enter Github access token (see here for instructions "
            "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token):"
        )
        self.config_file = {
            "github-access-token": github_token,
            "editor": "default",
            "repo-storage-directory": "default",
            "packages": {
                "webviz-core-components": {
                    "local": False,
                    "local_path": "",
                    "git_url": "https://github.com/equinor/webviz-core-components.git",
                    "branch": "origin/master",
                },
                "webviz-subsurface-components": {
                    "local": False,
                    "local_path": "",
                    "git_url": "https://github.com/equinor/webviz-subsurface-components.git",
                    "branch": "origin/master",
                },
                "webviz-config": {
                    "local": False,
                    "local_path": "",
                    "git_url": "https://github.com/equinor/webviz-config.git",
                    "branch": "origin/master",
                },
                "webviz-subsurface": {
                    "local": False,
                    "local_path": "",
                    "git_url": "https://github.com/equinor/webviz-subsurface.git",
                    "branch": "origin/master",
                },
            },
        }
        with open(self.config_file_path, encoding="utf-8", mode="a") as file:
            yaml.dump(self.config_file, file)

    def get_path(self) -> str:
        return self.config_file_path

    def get_repo_storage_directory(self) -> Optional[Path]:
        if not self.config_file or "repo-storage-directory" not in self.config_file:
            return None

        if (
            self.config_file["repo-storage-directory"] == "default"
            or not pathlib.Path(self.config_file["repo-storage-directory"]).exists()
        ):
            return user_data_dir()

        return pathlib.Path(self.config_file["repo-storage-directory"])

    def get_github_access_token(self) -> Optional[Path]:
        if not self.config_file or "github-access-token" not in self.config_file:
            return None

        return self.config_file["github-access-token"]

    def get_package(self, name: str) -> Optional[dict]:
        if (
            not self.config_file
            or "packages" not in self.config_file
            or name not in self.config_file["packages"]
        ):
            return None

        package = self.config_file["packages"][name]

        return package

    def get_preferred_editor(self) -> Optional[str]:
        if (
            not self.config_file
            or "editor" not in self.config_file
            or self.config_file["editor"] == "default"
        ):
            return None

        return self.config_file["editor"]
