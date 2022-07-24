"""Test of execute_clang_tidy.py.
"""

import copy
import pathlib

import trio
import trio.testing

from clang_tidy_checker.config import Config
from clang_tidy_checker.execute_clang_tidy import execute_clang_tidy


@trio.testing.trio_test
async def test_execute_clang_tidy_no_error(
    default_config: Config, sample_proj_no_error: pathlib.Path
):
    """Test of execute_clang_tidy resulting in no error."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_no_error / "build")
    input_file = str(sample_proj_no_error / "src" / "main.cpp")

    result = await execute_clang_tidy(config=config, input_file=input_file)

    assert result.input_file == input_file
    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr == ""
