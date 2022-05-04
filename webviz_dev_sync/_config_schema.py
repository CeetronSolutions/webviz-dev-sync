from typing import TypedDict, List
from ._github_manager import GithubManager


class GithubRepositoryNotFound(Exception):
    pass


class Package(TypedDict):
    name: str
    github_repo_name: str
    github_manager: GithubManager


def create_schema(github_access_token: str) -> dict:
    packages: List[Package] = [{
        "name": "webviz-core-components",
        "github_repo_name": "equinor/webviz-core-components",
        "github_manager": GithubManager(github_access_token)
    },
        {
        "name": "webviz-config",
        "github_repo_name": "equinor/webviz-config",
        "github_manager": GithubManager(github_access_token)
    },
        {
        "name": "webviz-subsurface-components",
        "github_repo_name": "equinor/webviz-subsurface-components",
        "github_manager": GithubManager(github_access_token)
    },
        {
        "name": "webviz-subsurface",
        "github_repo_name": "equinor/webviz-subsurface",
        "github_manager": GithubManager(github_access_token)
    }]

    for package in packages:
        if not package["github_manager"].open_repo(package["github_repo_name"]):
            raise GithubRepositoryNotFound(
                "equinor/webviz-core-components not found on Github")

    schema = {
        "$id": "https://github.com/equinor/webviz-dev-sync",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "required": ["editor", "github-access-token", "repo-storage-directory", "packages"],
        "additionalProperties": False,
        "properties": {
            "editor": {"type": "string"},
            "github-access-token": {"type": "string"},
            "repo-storage-directory": {"type": "string"},
            "packages": {
                "type": "object",
                "required": [package["name"] for package in packages],
                "properties": {
                    **{
                        package["name"]: {
                            "type": "object",
                            "oneOf": [
                                {
                                    "required": ["local_path"]
                                },
                                {
                                    "required": ["github_branch"]
                                }
                            ],
                            "additionalProperties": True,
                            "properties": {
                                "link_package": { "type": "boolean" },
                                "local_path": {"type": "string"},
                                "github_branch": {
                                    "type": "object",
                                    "oneOf": [
                                        {
                                            "properties": {
                                                "repository": {
                                                    "type": "string",
                                                    "enum": [repo["name"]],
                                                },
                                                "branch": {
                                                    "type": "string",
                                                    "enum": [branch.name for branch in repo["branches"]]
                                                }
                                            },
                                            "required": ["repository", "branch"],
                                            "additionalProperties": False,
                                        }
                                        for repo in package["github_manager"].get_all_branches()
                                    ],
                                },
                            },
                        }
                        for package in packages
                    }
                }
            }
        }
    }

    return schema
