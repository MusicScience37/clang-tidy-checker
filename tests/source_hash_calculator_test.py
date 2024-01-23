"""Test of source_hash_calculator.py"""

import copy
import pathlib

import pytest

from clang_tidy_checker.config import Config
from clang_tidy_checker.source_hash_calculator import SourceHashCalculator


@pytest.mark.asyncio
async def test_calculate_hash(
    default_config: Config, sample_proj_no_error: pathlib.Path
) -> None:
    """Test to calculate a hash."""
    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_no_error / "build")

    async with SourceHashCalculator(config=config) as calculator:
        input_file1 = str(sample_proj_no_error / "src" / "sample_function.cpp")
        input_file2 = str(sample_proj_no_error / "src" / "main.cpp")
        hash1 = await calculator.calculate(input_file1)
        hash2 = await calculator.calculate(input_file2)
        hash3 = await calculator.calculate(input_file1)
        assert hash1 != hash2
        assert hash1 == hash3
