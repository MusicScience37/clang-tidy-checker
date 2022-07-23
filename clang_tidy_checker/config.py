"""Configuration of this tool.
"""

import dataclasses

from clang_tidy_checker.search_clang_tidy import search_clang_tidy


@dataclasses.dataclass
class Config:
    """Class of configuration."""

    clang_tidy_path: str = "clang-tidy"


async def parse_config_from_dict(config: dict) -> Config:
    """Parse configuration from dictionaries.

    Args:
        config (dict): Input dictionary.

    Returns:
        Config: Configuration.
    """

    clang_tidy_path = config.get("clang_tidy_executable", "clang-tidy")
    clang_tidy_path = await search_clang_tidy(clang_tidy_path)

    return Config(clang_tidy_path=clang_tidy_path)
