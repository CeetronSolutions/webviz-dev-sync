from typing import Optional
import pathlib
import os
import sys
from subprocess import run, PIPE, check_call, check_output

from git import Repo, Remote
from git.exc import InvalidGitRepositoryError

from ._config_file import ConfigFile
from ._github_manager import GithubManager
from ._cache import Cache


class PackageManager:
    def __init__(self, name: str) -> None:
        self._name = name
        self._config = ConfigFile().get_package(name)
        self._github_manager = None
        self._repo: Optional[Repo] = None
        self._branch = None
        self._cache = Cache()

        if not self._config:
            return

        if self.is_local_package():
            self._path = self._config["local_path"]
        else:
            self._path = pathlib.Path.joinpath(
                ConfigFile().get_repo_storage_directory(), self._name
            )
            if not self._path.exists():
                self._path.mkdir()

            self._github_manager = GithubManager(ConfigFile().get_github_access_token())

            self.checkout()

    def checkout(self) -> None:
        if self._github_manager and self._path:
            self._github_manager.open_repo(self._config["github_branch"]["repository"])
            clone_url = self._github_manager.get_clone_url()

            try:
                self._repo = Repo(self._path)
                remote = Remote(
                    self._repo,
                    self._config["github_branch"]["repository"].split("/")[0],
                )
                if not remote.exists():
                    remote = remote.add(
                        repo=self._repo,
                        name=self._config["github_branch"]["repository"].split("/")[0],
                        url=clone_url,
                    )

                self._repo = remote.repo
            except InvalidGitRepositoryError:
                self._repo = Repo.clone_from(clone_url, self._path)
                remote = self._repo.remote()
                remote.rename(self._config["github_branch"]["repository"].split("/")[0])

            remote.fetch()

            self._repo.git.checkout(
                self._config["github_branch"]["repository"].split("/")[0]
                + "/"
                + self._config["github_branch"]["branch"]
            )

    def get_last_modified_date(self) -> float:
        return os.path.getmtime(self._path)

    def is_node_package(self) -> bool:
        return pathlib.Path.joinpath(self._path, "react").is_dir()

    def is_local_package(self) -> bool:
        return "local_path" in self._config

    def install(self) -> None:
        if self._cache.get_package_modified_timestamp(
            self._name, self.is_local_package()
        ) < os.path.getmtime(self._path):
            print(f"Installing '{self._name}'...")
            if sys.platform.startswith("win"):
                check_call(["npm", "config", "set", "script-shell", "powershell"])
            self.execute_package_specific_installation_routine()
            self._cache.store_package_modified_timestamp(
                self._name, self.is_local_package()
            )

    def execute_package_specific_installation_routine(self) -> None:
        raise NotImplementedError

    def execute_package_specific_build_routine(self) -> None:
        raise NotImplementedError

    def get_build_timestamp(self) -> float:
        raise NotImplementedError

    def build(self) -> None:
        if (
            self._cache.get_package_build_timestamp(self._name, self.is_local_package())
            < self.get_build_timestamp()
        ):
            self.execute_package_specific_build_routine()
            self._cache.store_package_built_timestamp(
                self._name, self.is_local_package()
            )

    def is_linked(self) -> bool:
        linked_packages = check_output(
            ["npm", "ls", "-g", "--depth=0", "--link=true"], cwd=self._path
        )
        path = (
            str(self._path)[0 : len(str(self._path)) - 1]
            if str(self._path)[len(str(self._path)) - 1] == "/"
            else str(self._path)
        )
        return path in str(linked_packages)

    def is_linked_to(self, other_package: str, other_package_path: str = "") -> bool:
        packages = run(
            ["npm", "list"],
            cwd=os.path.join(self._path, "react"),
            stdout=PIPE,
        ).stdout
        path = (
            other_package_path[0 : len(other_package_path) - 1]
            if other_package_path[len(other_package_path) - 1] == "/"
            else other_package_path
        )
        for line in str(packages).split("\\n"):
            if other_package in line and (path in line or other_package_path == ""):
                return True
        return False

    def shall_be_linked(self) -> bool:
        return not (
            "link_package" in self._config and self._config["link_package"] == False
        )

    @property
    def path(self) -> pathlib.PosixPath:
        return self._path
