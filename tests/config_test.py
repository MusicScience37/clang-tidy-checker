"""Test of config.py
"""

import trio
import trio.testing

from clang_tidy_checker.config import parse_config_from_dict


@trio.testing.trio_test
async def test_parse_config_from_dict_default():
    """Test of parse_config_from_dict for default configuration."""

    input_config = {}

    output = await parse_config_from_dict(input_config)

    assert "clang-tidy" in output.clang_tidy_path
    assert not await trio.Path(output.clang_tidy_path).is_symlink()
    assert await trio.Path(output.clang_tidy_path).is_file()


@trio.testing.trio_test
async def test_parse_config_from_dict_search_clang_tidy():
    """Test of parse_config_from_dict to search clang-tidy executable."""

    # use different command for test
    input_config = {"clang_tidy_executable": "gcc"}

    output = await parse_config_from_dict(input_config)

    assert "gcc" in output.clang_tidy_path
    assert not await trio.Path(output.clang_tidy_path).is_symlink()
    assert await trio.Path(output.clang_tidy_path).is_file()
