"""Search checked files.
"""

import pathlib
import typing

from clang_tidy_checker.config import Config


async def search_checked_files(*, config: Config) -> typing.List[str]:
    """Search checked files.

    Args:
        config (Config): Configuration.

    Returns:
        typing.List[str]: Checked files.
    """

    checked_files: typing.List[str] = []

    cwd = pathlib.Path.cwd()
    cwd = cwd.absolute()

    for pattern in config.checked_file_patterns:
        paths = cwd.glob(pattern)
        checked_files += sorted([str(path.absolute()) for path in paths])

    return checked_files
