from typing import TypedDict, List
import github
from github.PaginatedList import PaginatedList

from .config_file import ConfigFile


class Repository(TypedDict):
    name: str
    branches: List[str]


class GithubManager:
    def __init__(self, repo_name: str) -> None:
        self._github = github.Github(ConfigFile().get_github_access_token())
        self._repo = self._github.get_repo(repo_name)

    def get_forks(self) -> PaginatedList:
        return self._repo.get_forks()

    def get_all_branches(self) -> List[Repository]:
        repositories: List[Repository] = []
        for fork in self.get_forks():
            repositories.append(
                {"name": fork.full_name, "branches": list(fork.get_branches())}
            )
        return repositories
