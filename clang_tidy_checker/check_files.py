"""Check files.
"""

import typing

import tqdm
import tqdm.contrib.logging

from clang_tidy_checker.config import Config
from clang_tidy_checker.execute_clang_tidy import execute_clang_tidy


async def check_files(*, config: Config, input_files: typing.List[str]) -> bool:
    """Check files.

    Args:
        config (Config): Configuration.
        input_files (typing.List[str]): Files.

    Returns:
        bool: True if no error, False otherwise.
    """

    has_error = False

    with tqdm.contrib.logging.logging_redirect_tqdm():
        tqdm_obj = tqdm.tqdm(
            total=len(input_files), unit="file", disable=not config.show_progress
        )
        # TODO: multiple files at once.
        for input_file in input_files:
            result = await execute_clang_tidy(config=config, input_file=input_file)
            if result.exit_code != 0:
                has_error = True
            tqdm_obj.update()
        tqdm_obj.close()

    return not has_error
