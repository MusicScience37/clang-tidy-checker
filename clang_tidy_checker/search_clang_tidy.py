"""Search clang-tidy executable.
"""

import logging
import pathlib
import shutil

LOGGER = logging.getLogger(__name__)


async def search_clang_tidy(name_or_path: str) -> str:
    """Search clang-tidy executable.

    Args:
        name_or_path (str): Name or path of clang-tidy.

    Returns:
        str: Full path of clang-tidy executable to use.
    """

    path = pathlib.Path(name_or_path)
    if not path.exists():
        found_path = shutil.which(name_or_path)
        if not found_path:
            raise RuntimeError("Failed to find clang-tidy executable.")
        path = pathlib.Path(found_path)

    while path.is_symlink():
        path = path.resolve()

    LOGGER.debug("clang-tidy found at %s", path)

    return str(path)
