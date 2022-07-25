"""Search checked files.
"""

import typing

import trio

from clang_tidy_checker.config import Config


async def search_checked_files(*, config: Config) -> typing.List[str]:
    """Search checked files.

    Args:
        config (Config): Configuration.

    Returns:
        typing.List[str]: Checked files.
    """

    checked_files: typing.List[str] = []

    cwd = await trio.Path.cwd()
    cwd = await cwd.absolute()

    for pattern in config.checked_file_patterns:
        paths = await cwd.glob(pattern)
        checked_files += sorted([str(await path.absolute()) for path in paths])

    return checked_files
