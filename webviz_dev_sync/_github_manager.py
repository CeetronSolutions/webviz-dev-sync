from typing import TypedDict, List, Optional
from github import Github, UnknownObjectException
from github.Repository import Repository
from github.Branch import Branch
from github.PaginatedList import PaginatedList


class RepositoryBranches(TypedDict):
    name: str
    branches: List[Branch]


class GithubManager:
    def __init__(self, access_token: str) -> None:
        self._github = Github(access_token)
        self._repo: Optional[Repository] = None

    def open_repo(self, repo_name: str) -> bool:
        try:
            self._repo = self._github.get_repo(repo_name)
            return True
        except UnknownObjectException:
            self._repo = None
        return False

    def exists(self) -> bool:
        return self._repo != None

    def get_forks(self) -> Optional[PaginatedList]:
        if self._repo:
            return self._repo.get_forks()
        return None

    def get_clone_url(self) -> str:
        if self._repo:
            return self._repo.clone_url
        return ""

    def get_all_branches(self) -> List[RepositoryBranches]:
        repositories: List[RepositoryBranches] = []
        if self._repo:
            repositories.append(
                {
                    "name": self._repo.full_name,
                    "branches": list(self._repo.get_branches()),
                }
            )
            forks = self.get_forks()
            if forks:
                for fork in forks:
                    repositories.append(
                        {"name": fork.full_name, "branches": list(fork.get_branches())}
                    )
        return repositories
