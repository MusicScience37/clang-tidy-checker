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

# Key of extra arguments.
EXTRA_ARGS_KEY = "extra_args"

# Key of cache directory.
CACHE_DIR_KEY = "cache_dir"

# Key of the maximum number of entries in the cache.
MAX_CACHE_ENTRIES_KEY = "max_cache_entries"

# Default value of the maximum number of entries in the cache.
DEFAULT_MAX_CACHE_ENTRIES_KEY = 1000


@dataclasses.dataclass
class Config:
    """Class of configuration."""

    clang_tidy_path: str
    build_dir: str
    show_progress: bool
    checked_file_patterns: typing.List[str]
    extra_args: typing.List[str]
    cache_dir: typing.Optional[str]
    max_cache_entries: int


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

    extra_args = [str(elem) for elem in config.get(EXTRA_ARGS_KEY, [])]

    cache_dir = config.get(CACHE_DIR_KEY, None)
    if cache_dir is not None:
        cache_dir = str(cache_dir)

    max_cache_entries = int(
        config.get(MAX_CACHE_ENTRIES_KEY, DEFAULT_MAX_CACHE_ENTRIES_KEY)
    )

    return Config(
        clang_tidy_path=clang_tidy_path,
        build_dir=build_dir,
        show_progress=show_progress,
        checked_file_patterns=checked_file_patterns,
        extra_args=extra_args,
        cache_dir=cache_dir,
        max_cache_entries=max_cache_entries,
    )
