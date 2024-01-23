"""Test of check_files.py.
"""

import copy
import pathlib

import pytest

from clang_tidy_checker.check_files import check_files
from clang_tidy_checker.config import Config


@pytest.mark.asyncio
async def test_check_files_no_error(
    default_config: Config, sample_proj_no_error: pathlib.Path
):
    """Test of check_files without errors."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_no_error / "build")
    input_files = [
        str(sample_proj_no_error / "src" / "sample_function.cpp"),
        str(sample_proj_no_error / "src" / "main.cpp"),
    ]

    result = await check_files(config=config, input_files=input_files)

    assert result


@pytest.mark.asyncio
async def test_check_files_warning(
    default_config: Config, sample_proj_warning: pathlib.Path
):
    """Test of check_files with a warning."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_warning / "build")
    input_files = [
        str(sample_proj_warning / "src" / "sample_function.cpp"),
        str(sample_proj_warning / "src" / "main.cpp"),
    ]

    result = await check_files(config=config, input_files=input_files)

    assert not result


@pytest.mark.asyncio
async def test_check_files_error(
    default_config: Config, sample_proj_error: pathlib.Path
):
    """Test of check_files with an error."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_error / "build")
    input_files = [
        str(sample_proj_error / "src" / "sample_function.cpp"),
        str(sample_proj_error / "src" / "main.cpp"),
    ]

    result = await check_files(config=config, input_files=input_files)

    assert not result
