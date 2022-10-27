import dataclasses
import subprocess

from typing import Union

from pyreleaser.util.types import PathType

ENCODING = "utf-8"


@dataclasses.dataclass
class ProcessResult:
    """
    Utility class that wraps a subprocess CompletedProcess
    """

    stdout: str
    stderr: str
    exit_code: int

    @classmethod
    def parse(
        cls,
        completed_process: Union[
            subprocess.CompletedProcess, subprocess.CompletedProcess[bytes]
        ],
    ):
        stdout = completed_process.stdout.decode(ENCODING).rstrip("\n")
        stderr = completed_process.stderr.decode(ENCODING).rstrip("\n")
        exit_code = completed_process.returncode
        return cls(stdout, stderr, exit_code)


def execute_process(args: list[str], cwd: PathType = None) -> ProcessResult:
    """
    Execute a process with the given args, if cwd is provided the process will
    run in that directory
    :param args: a list of str values
    :param cwd: the directory to execute the process in
    :return: returns a ProcessResult
    """
    result = subprocess.run(
        args=args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return ProcessResult.parse(result)
