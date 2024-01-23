"""Main function.
"""

import asyncio
import logging
import os
import sys
import typing

import click
import yaml

from clang_tidy_checker.check_files import check_files
from clang_tidy_checker.config import (
    BUILD_DIR_KEY,
    CACHE_DIR_KEY,
    CHECKED_FILE_PATTERNS_KEY,
    EXTRA_ARGS_KEY,
    SHOW_PROGRESS_KEY,
    parse_config_from_dict,
)
from clang_tidy_checker.search_checked_files import search_checked_files

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
        if config_file != "" and os.path.exists(config_file):
            with open(config_file, mode="r", encoding="utf8") as file:
                return yaml.safe_load(file)
    return {}


@click.command()
@click.option("--config", "-c", default="", help="Configuration file path.")
@click.option("--build_dir", "-b", default="", help="Build directory.")
@click.option("--pattern", "-p", multiple=True, help="Checked file pattern.")
@click.option(
    "--extra_arg", multiple=True, help="Extra argument to clang-tidy command."
)
@click.option("--cache_dir", default="", help="Cache directory.")
@click.option(
    "--no-ascii", is_flag=True, help="Prevent writing ASCII escape sequences."
)
def main(  # pylint: disable=too-many-arguments
    config: str,
    build_dir: str,
    pattern: typing.List[str],
    extra_arg: typing.List[str],
    cache_dir: str,
    no_ascii: bool,
):
    """Check files using clang-tidy."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    config_dict = load_config_file(config, ".clang-tidy-checker")
    if build_dir != "":
        config_dict[BUILD_DIR_KEY] = build_dir
    if pattern:
        config_dict[CHECKED_FILE_PATTERNS_KEY] = pattern
    if extra_arg:
        config_dict[EXTRA_ARGS_KEY] = extra_arg
    if cache_dir:
        config_dict[CACHE_DIR_KEY] = cache_dir
    if no_ascii:
        config_dict[SHOW_PROGRESS_KEY] = False

    is_success = asyncio.run(async_main(config_dict))

    if is_success:
        LOGGER.info("No error detected.")
        sys.exit(0)
    else:
        LOGGER.error("Some errors detected.")
        sys.exit(1)
