"""Main function.
"""

import logging
import os
import sys
import typing

import click
import trio
import yaml

from clang_tidy_checker.check_files import check_files
from clang_tidy_checker.config import (
    parse_config_from_dict,
    BUILD_DIR_KEY,
    CHECKED_FILE_PATTERNS_KEY,
    SHOW_PROGRESS_KEY,
)
from clang_tidy_checker.search_checked_files import search_checked_files

try:
    from yaml import CLoader as YamlLoader  # type: ignore
except ImportError:
    from yaml import Loader as YamlLoader  # type: ignore

LOGGER = logging.getLogger(__name__)


async def async_main(config_dict: dict) -> bool:
    """Main function.

    Args:
        config_dict (dict): Dictionary of the configuration.

    Returns:
        bool: True if no error, False otherwise.
    """

    config = await parse_config_from_dict(config_dict)
    checked_files = await search_checked_files(config=config)
    return await check_files(config=config, input_files=checked_files)


def load_config_file(*config_files) -> dict:
    """Load configuration file.

    The first existing file is loaded.

    Returns:
        dict: Dictionary of the configuration.
    """

    for config_file in config_files:
        if os.path.exists(config_file):
            with open(config_file, mode="r", encoding="utf8") as file:
                return yaml.load(file, YamlLoader)
    return {}


@click.command()
@click.option("--config", "-c", default="", help="Configuration file path.")
@click.option("--build_dir", "-b", default="", help="Build directory.")
@click.option("--pattern", "-p", multiple=True, help="Checked file pattern.")
@click.option(
    "--no-ascii", is_flag=True, help="Prevent writing ASCII escape sequences."
)
def main(config: str, build_dir: str, pattern: typing.List[str], no_ascii: bool):
    """Check files using clang-tidy."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    config_dict = load_config_file(".clang-tidy-checker", config)
    if build_dir != "":
        config_dict[BUILD_DIR_KEY] = build_dir
    if pattern:
        config_dict[CHECKED_FILE_PATTERNS_KEY] = pattern
    if no_ascii:
        config_dict[SHOW_PROGRESS_KEY] = False

    is_success = trio.run(async_main, config_dict)

    if is_success:
        LOGGER.info("No error detected.")
        sys.exit(0)
    else:
        LOGGER.error("Some errors detected.")
        sys.exit(1)
