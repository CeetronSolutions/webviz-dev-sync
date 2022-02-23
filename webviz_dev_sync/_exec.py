from typing import List
from pathlib import Path
from subprocess import run, PIPE, CalledProcessError, STDOUT

from ._user_data_dir import user_data_dir


def exec(args: List[str], cwd: Path, shell: bool = False) -> None:

    with open(Path.joinpath(user_data_dir(), ".build.log"), "a") as log:
        log.write(
            "\n\n"
            + "-------------------------------------------\n"
            + " ".join(args)
            + "\n-------------------------------------------\n\n"
        )
        result = run(" ".join(args), cwd=cwd, shell=shell, stdout=PIPE, stderr=STDOUT)
        log.write(result.stdout.decode("utf-8"))
        if not result.returncode == 0:
            raise CalledProcessError(result.returncode, " ".join(args), result.stderr)


def check_output(args: List[str], cwd: Path, shell: bool = False) -> str:
    with open(Path.joinpath(user_data_dir(), ".build.log"), "a") as log:
        log.write(
            "\n\n"
            + "-------------------------------------------\n"
            + " ".join(args)
            + "\n-------------------------------------------\n\n"
        )
        result = run(" ".join(args), cwd=cwd, shell=shell, stdout=PIPE, stderr=STDOUT)
        log.write(result.stdout.decode("utf-8"))
        return result.stdout.decode("utf-8")
