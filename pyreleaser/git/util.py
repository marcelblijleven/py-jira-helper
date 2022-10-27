from typing import Optional

from pyreleaser.util.process import execute_process
from pyreleaser.util.types import PathType


def get_current_tag(cwd: Optional[PathType]) -> str:
    """
    Retrieves the current Git tag
    :param cwd: optional directory to retrieve tag from
    """
    if (
        result := execute_process(
            args=["git", "describe", "--tags", "--abbrev=0"],
            cwd=cwd,
        )
    ).exit_code != 0:
        raise SystemExit(f"Error received while retrieving tag: {result.stderr}")

    return result.stdout


def get_previous_tag(current_tag: str, cwd: Optional[PathType]) -> str:
    """
    Retrieves the previous tag based on the provided current tag
    :param current_tag: the current tag
    :param cwd: optional directory to retrieve tag from
    """
    if (
        result := execute_process(
            args=["git", "describe", "--tags", "--abbrev=0", f"{current_tag}^"],
            cwd=cwd,
        )
    ).exit_code != 0:
        raise SystemExit(f"Error received while retrieving tag: {result.stderr}")

    return result.stdout


def get_commits_between_tags(tag_a: str, tag_b: str, cwd: Optional[PathType]) -> str:
    """
    Retrieves commits between the two provided tags
    :param tag_a: the previous tag
    :param tag_b: the current tag
    :param cwd: optional directory to retrieve tag from
    """
    if (
        result := execute_process(
            args=["git", "log", "--oneline", f"{tag_a}..{tag_b}"],
            cwd=cwd,
        )
    ).exit_code != 0:
        raise SystemExit(f"Error received while retrieving commits: {result.stderr}")

    return result.stdout
