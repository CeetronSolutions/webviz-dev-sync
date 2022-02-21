from typing import List
from pathlib import Path
import sys
from subprocess import run, PIPE, CalledProcessError

from ._user_data_dir import user_data_dir

def exec(args: List[str], cwd: Path, shell: bool = False) -> None:

    with open(Path.joinpath(user_data_dir(), ".build.log"), "a") as log:
        log.write("\n\n" + "-------------------------------------------\n" + " ".join(args) + "\n-------------------------------------------\n\n")
        result = run(args, cwd=cwd, shell=shell, stdout=PIPE)
        print(result.stdout.decode("utf-8"))
        log.write(result.stdout.decode("utf-8"))
        if not result.returncode == 0:
            raise CalledProcessError(result.returncode, args, result.stderr)