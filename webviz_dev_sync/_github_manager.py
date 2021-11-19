from typing import TypedDict, List
import github
from github.PaginatedList import PaginatedList


class Repository(TypedDict):
    name: str
    branches: List["github.Branch"]


class GithubManager:
    def __init__(self, access_token: str) -> None:
        self._github = github.Github(access_token)

    def open_repo(self, repo_name: str) -> bool:
        try:
            self._repo = self._github.get_repo(repo_name)
            return True
        except github.UnknownObjectException:
            self._repo = None
        return False

    def exists(self) -> bool:
        return self._repo != None

    def get_forks(self) -> PaginatedList:
        return self._repo.get_forks()

    def get_clone_url(self) -> str:
        return self._repo.clone_url

    def get_all_branches(self) -> List[Repository]:
        repositories: List[Repository] = []
        repositories.append(
            {"name": self._repo.full_name, "branches": list(
                self._repo.get_branches())}
        )
        for fork in self.get_forks():
            repositories.append(
                {"name": fork.full_name, "branches": list(fork.get_branches())}
            )
        return repositories
