"""Configuration of this tool.
"""

import dataclasses
import typing

from clang_tidy_checker.search_clang_tidy import search_clang_tidy

# Key of the name of clang-tidy executable to use.
CLANG_TIDY_EXECUTABLE_KEY = "clang_tidy_executable"

# Default name of clang-tidy executable to use.
DEFAULT_CLANG_TIDY_EXECUTABLE = "clang-tidy"

# Key of the path of the build directory.
BUILD_DIR_KEY = "build_dir"

# Default path of the build directory.
DEFAULT_BUILD_DIR = "build"

# Key of the flag to show progress.
SHOW_PROGRESS_KEY = "show_progress"

# Default flag value to show progress.
DEFAULT_SHOW_PROGRESS = True

# Key of checked file patterns.
CHECKED_FILE_PATTERNS_KEY = "file_patterns"

# Default checked files.
DEFAULT_CHECKED_FILE_PATTERNS = [
    "**/*.c",
    "**/*.cpp",
    "**/*.cxx",
    "**/*.cc",
]


@dataclasses.dataclass
class Config:
    """Class of configuration."""

    clang_tidy_path: str
    build_dir: str
    show_progress: bool
    checked_file_patterns: typing.List[str]


async def parse_config_from_dict(config: dict) -> Config:
    """Parse configuration from dictionaries.

    Args:
        config (dict): Input dictionary.

    Returns:
        Config: Configuration.
    """

    clang_tidy_path = str(
        config.get(CLANG_TIDY_EXECUTABLE_KEY, DEFAULT_CLANG_TIDY_EXECUTABLE)
    )
    clang_tidy_path = await search_clang_tidy(clang_tidy_path)

    build_dir = str(config.get(BUILD_DIR_KEY, DEFAULT_BUILD_DIR))

    show_progress = bool(config.get(SHOW_PROGRESS_KEY, DEFAULT_SHOW_PROGRESS))

    checked_file_patterns = list(
        config.get(CHECKED_FILE_PATTERNS_KEY, DEFAULT_CHECKED_FILE_PATTERNS)
    )

    return Config(
        clang_tidy_path=clang_tidy_path,
        build_dir=build_dir,
        show_progress=show_progress,
        checked_file_patterns=checked_file_patterns,
    )
