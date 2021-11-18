from git import Repo
import pathlib

from git.exc import InvalidGitRepositoryError

from .config_file import ConfigFile


class PackageManager:
    def __init__(self, name: str) -> None:
        self._config = ConfigFile().get_package(name)
        self._repo = None
        self._branch = None
        if not self._config:
            return

        if self._config["local"]:
            self._path = self._config["local_path"]
        else:
            self._path = pathlib.Path.joinpath(
                ConfigFile().get_repo_storage_directory(), name
            )
            if not self._path.exists():
                self._path.mkdir()

            try:
                self._repo = Repo(self._path)
            except InvalidGitRepositoryError:
                self._repo = Repo.clone_from(self._config["git_url"], self._path)

            if (
                not f"{self._repo.remote()}/{self._repo.active_branch.name}"
                == self._config["branch"]
            ):
                pass
