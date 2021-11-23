import os
import re
import pathlib

from setuptools import setup, find_packages


def get_long_description() -> str:
    """Converts relative repository links to absolute URLs
    if GITHUB_REPOSITORY and GITHUB_SHA environment variables exist.
    If not, it returns the raw content in README.md.
    """

    raw_readme = pathlib.Path("README.md").read_text()

    repository = os.environ.get("GITHUB_REPOSITORY")
    sha = os.environ.get("GITHUB_SHA")

    if repository is not None and sha is not None:
        full_url = f"https://github.com/{repository}/blob/{sha}/"
        return re.sub(r"]\((?!https)", "](" + full_url, raw_readme)
    return raw_readme


# pylint: disable=line-too-long
setup(
    name="webviz-dev-sync",
    description="Developer tool for syncing webviz packages",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/equinor/webviz-dev-sync",
    author="R&T Equinor",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "webviz_dev_sync": [
            "py.typed",
        ]
    },
    entry_points={
        "console_scripts": ["webviz-dev=webviz_dev_sync.command_line:main"],
    },
    install_requires=[
        "gitpython>=3.1.18",
        "watchdog>=2.1.6",
        "PyGithub>=1.55",
        "pyyaml>=5.4.1",
        "jsonschema>=4.0.0",
        "pysimplegui>=4.55.1"
    ],
    setup_requires=["setuptools_scm~=3.2"],
    python_requires="~=3.6",
    use_scm_version=True,
    zip_safe=False,
    project_urls={
        "Documentation": "https://equinor.github.io/webviz-dev-sync",
        "Download": "https://equinor.github.io/webviz-dev-sync",
        "Source": "https://equinor.github.io/webviz-dev-sync",
        "Tracker": "https://equinor.github.io/webviz-dev-sync/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
    ],
)
