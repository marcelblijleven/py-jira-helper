import os

from pyreleaser.util.types import PathType


def path_exists(path: PathType) -> bool:
    return os.path.exists(path)
