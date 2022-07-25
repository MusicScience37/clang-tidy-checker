"""Search clang-tidy executable.
"""

import shutil
import logging

import trio

LOGGER = logging.getLogger(__name__)


async def search_clang_tidy(name_or_path: str) -> str:
    """Search clang-tidy executable.

    Args:
        name_or_path (str): Name or path of clang-tidy.

    Returns:
        str: Full path of clang-tidy executable to use.
    """

    path = trio.Path(name_or_path)
    if not await path.exists():
        found_path = shutil.which(name_or_path)
        if not found_path:
            raise RuntimeError("Failed to find clang-tidy executable.")
        path = trio.Path(found_path)

    while await path.is_symlink():
        path = await path.resolve()

    LOGGER.debug("clang-tidy found at %s", path)

    return str(path)
