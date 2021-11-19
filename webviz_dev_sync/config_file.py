from pathlib import Path
import yaml
from typing import Optional
from jsonschema import validate, ValidationError
from getpass import getpass
import os

from ._user_data_dir import user_data_dir
from ._config_schema import create_schema


class ConfigFile:
    def __init__(self) -> None:
        self._config_file_path = Path.joinpath(user_data_dir(), "config.yaml")
        self._config_file = None
        if not self._config_file_path.exists():
            Path.mkdir(user_data_dir(), exist_ok=True)
            self.make_default_file()
        else:
            with open(self._config_file_path, encoding="utf-8", mode="r") as file:
                self._config_file = yaml.safe_load(file)

    def check_validity(self) -> bool:
        if not self._config_file:
            return False

        try:
            validate(self._config_file, create_schema(
                self.get_github_access_token()))
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
        self._config_file = {
            "github-access-token": github_token,
            "editor": "default",
            "repo-storage-directory": "default",
            "packages": {
                "webviz-core-components": {
                    "github_branch": {
                        "repository": "equinor/webviz-core-components",
                        "branch": "master",
                    }
                },
                "webviz-subsurface-components": {
                    "github_branch": {
                        "repository": "equinor/webviz-subsurface-components",
                        "branch": "master",
                    }
                },
                "webviz-config": {
                    "github_branch": {
                        "repository": "equinor/webviz-config",
                        "branch": "master",
                    }
                },
                "webviz-subsurface": {
                    "github_branch": {
                        "repository": "equinor/webviz-subsurface",
                        "branch": "master",
                    }
                },
            },
        }
        with open(self._config_file_path, encoding="utf-8", mode="a") as file:
            yaml.dump(self._config_file, file)

    def get_last_modified_ms(self) -> float:
        return os.path.getmtime(self._config_file_path)

    def get_path(self) -> str:
        return self._config_file_path

    def get_repo_storage_directory(self) -> Optional[Path]:
        if not self._config_file or "repo-storage-directory" not in self._config_file:
            return None

        if (
            self._config_file["repo-storage-directory"] == "default"
            or not Path(self._config_file["repo-storage-directory"]).exists()
        ):
            return user_data_dir()

        return Path(self._config_file["repo-storage-directory"])

    def get_github_access_token(self) -> Optional[Path]:
        if not self._config_file or "github-access-token" not in self._config_file:
            return None

        return self._config_file["github-access-token"]

    def get_package(self, name: str) -> Optional[dict]:
        if (
            not self._config_file
            or "packages" not in self._config_file
            or name not in self._config_file["packages"]
        ):
            return None

        package = self._config_file["packages"][name]

        return package

    def get_preferred_editor(self) -> Optional[str]:
        if (
            not self._config_file
            or "editor" not in self._config_file
            or self._config_file["editor"] == "default"
        ):
            return None

        return self._config_file["editor"]
