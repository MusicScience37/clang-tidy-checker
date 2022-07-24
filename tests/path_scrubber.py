"""Scrubber of paths.
"""

import pathlib


THIS_DIR = pathlib.Path(__file__).absolute().parent
ROOT_DIR = THIS_DIR.parent


def replace_root_dir(input: str) -> str:
    """Replace path of root directory.

    Args:
        input (str): Input.

    Returns:
        str: Output.
    """

    return input.replace(str(ROOT_DIR), "<root-dir>")


PATH_SCRUBBER = replace_root_dir
