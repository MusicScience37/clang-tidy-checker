"""Test of config.py
"""

import pathlib

import pytest

from clang_tidy_checker.config import (
    parse_config_from_dict,
    DEFAULT_CHECKED_FILE_PATTERNS,
)


@pytest.mark.asyncio
async def test_parse_config_from_dict_default():
    """Test of parse_config_from_dict for default configuration."""

    input_config = {}

    output = await parse_config_from_dict(input_config)

    assert "clang-tidy" in output.clang_tidy_path
    assert not pathlib.Path(output.clang_tidy_path).is_symlink()
    assert pathlib.Path(output.clang_tidy_path).is_file()

    assert output.build_dir == "build"

    assert output.show_progress

    assert output.checked_file_patterns == DEFAULT_CHECKED_FILE_PATTERNS


@pytest.mark.asyncio
async def test_parse_config_from_dict_search_clang_tidy():
    """Test of parse_config_from_dict to search clang-tidy executable."""

    # use different command for test
    input_config = {"clang_tidy_executable": "gcc"}

    output = await parse_config_from_dict(input_config)

    assert "gcc" in output.clang_tidy_path
    assert not pathlib.Path(output.clang_tidy_path).is_symlink()
    assert pathlib.Path(output.clang_tidy_path).is_file()

    assert output.build_dir == "build"

    assert output.show_progress

    assert output.checked_file_patterns == DEFAULT_CHECKED_FILE_PATTERNS


@pytest.mark.asyncio
async def test_parse_config_from_dict_with_build_dir():
    """Test of parse_config_from_dict with build_dir key."""

    input_config = {"build_dir": "build_test"}

    output = await parse_config_from_dict(input_config)

    assert "clang-tidy" in output.clang_tidy_path
    assert not pathlib.Path(output.clang_tidy_path).is_symlink()
    assert pathlib.Path(output.clang_tidy_path).is_file()

    assert output.build_dir == "build_test"

    assert output.show_progress

    assert output.checked_file_patterns == DEFAULT_CHECKED_FILE_PATTERNS


@pytest.mark.asyncio
async def test_parse_config_from_dict_without_progress():
    """Test of parse_config_from_dict without showing progress."""

    input_config = {"show_progress": False}

    output = await parse_config_from_dict(input_config)

    assert "clang-tidy" in output.clang_tidy_path
    assert not pathlib.Path(output.clang_tidy_path).is_symlink()
    assert pathlib.Path(output.clang_tidy_path).is_file()

    assert output.build_dir == "build"

    assert not output.show_progress

    assert output.checked_file_patterns == DEFAULT_CHECKED_FILE_PATTERNS


@pytest.mark.asyncio
async def test_parse_config_from_dict_with_checked_file_patterns():
    """Test of parse_config_from_dict with checked file patterns."""

    input_config = {"file_patterns": ["*.cpp"]}

    output = await parse_config_from_dict(input_config)

    assert "clang-tidy" in output.clang_tidy_path
    assert not pathlib.Path(output.clang_tidy_path).is_symlink()
    assert pathlib.Path(output.clang_tidy_path).is_file()

    assert output.build_dir == "build"

    assert output.show_progress

    assert output.checked_file_patterns == ["*.cpp"]
