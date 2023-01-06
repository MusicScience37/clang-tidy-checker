"""Test search_checked_files.py.
"""

import copy
import pathlib

import pytest

from clang_tidy_checker.config import Config
from clang_tidy_checker.search_checked_files import search_checked_files

THIS_DIR = pathlib.Path(__file__).absolute().parent
SAMPLE_DIR = THIS_DIR.parent / "sample_inputs"
RELATIVE_SAMPLE_DIR = SAMPLE_DIR.relative_to(pathlib.Path.cwd())


@pytest.mark.asyncio
async def test_search_checked_files(default_config: Config):
    """Test of search_checked_files."""

    config = copy.deepcopy(default_config)
    config.checked_file_patterns = [
        str(RELATIVE_SAMPLE_DIR / "proj_no_error" / "src" / "*.cpp"),
        str(RELATIVE_SAMPLE_DIR / "proj_error" / "src" / "**" / "*.cpp"),
    ]

    files = await search_checked_files(config=config)

    assert sorted(files) == sorted(
        [
            str(SAMPLE_DIR / "proj_no_error" / "src" / "sample_function.cpp"),
            str(SAMPLE_DIR / "proj_no_error" / "src" / "main.cpp"),
            str(SAMPLE_DIR / "proj_error" / "src" / "sample_function.cpp"),
            str(SAMPLE_DIR / "proj_error" / "src" / "main.cpp"),
        ]
    )
