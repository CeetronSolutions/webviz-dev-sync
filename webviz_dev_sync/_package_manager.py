from git import Repo, Remote
import pathlib
import os
import subprocess

from git.exc import InvalidGitRepositoryError

from .config_file import ConfigFile
from ._github_manager import GithubManager


class PackageManager:
    def __init__(self, name: str) -> None:
        self._name = name
        self._config = ConfigFile().get_package(name)
        self._github_manager = None
        self._repo = None
        self._branch = None
        if not self._config:
            return

        if "local_path" in self._config:
            self._path = self._config["local_path"]
        else:
            self._path = pathlib.Path.joinpath(
                ConfigFile().get_repo_storage_directory(), name
            )
            if not self._path.exists():
                self._path.mkdir()

            self._github_manager = GithubManager(
                ConfigFile().get_github_access_token())
            self._github_manager.open_repo(
                self._config["github_branch"]["repository"])
            clone_url = self._github_manager.get_clone_url()

            try:
                self._repo = Repo(self._path)
                remote = Remote(
                    self._repo, self._config["github_branch"]["repository"].split("/")[0])
                if not remote.exists():
                    remote = Remote.add(self._repo, self._config["github_branch"]["repository"].split(
                        "/")[0], clone_url)

                self._repo = remote.repo
            except InvalidGitRepositoryError:
                self._repo = Repo.clone_from(clone_url, self._path)
                remote = self._repo.remote()
                remote.rename(self._config["github_branch"]["repository"].split(
                    "/")[0])

            remote.fetch()

            self._repo.git.checkout(self._config["github_branch"]["repository"].split(
                "/")[0] + "/" + self._config["github_branch"]["branch"])

            # self._repo.active_branch.

    def get_last_modified_date(self) -> float:
        return os.path.getmtime(self._path)

    def is_node_package(self) -> bool:
        return pathlib.Path.joinpath(self._path, "react").is_dir()

    def install(self) -> None:
        subprocess.check_call(
            ["npm", "config", "set", "script-shell", "powershell"])

    def build(self) -> None:
        raise NotImplementedError
