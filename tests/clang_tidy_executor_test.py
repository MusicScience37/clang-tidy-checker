"""Test of clang_tidy_executor.py"""

import copy
import pathlib

import approvaltests
import approvaltests.scrubbers
import pytest

from clang_tidy_checker.clang_tidy_executor import (
    CachedClangTidyExecutor,
    CheckResult,
    ClangTidyExecutor,
)
from clang_tidy_checker.config import Config

from .path_scrubber import PATH_SCRUBBER
from .warning_count_scrubber import WARNING_COUNT_SCRUBBER


def check_result(input_file: str, result: CheckResult):
    """Check a result.

    Args:
        input_file (str): Input file path.
        result (ExecutionResult): Result.
    """

    approvaltests.approvals.verify(
        f"""input_file: {input_file}
exit_code: {result.exit_code}
stdout:
{result.stdout}
stderr:
{result.stderr}
""",
        options=approvaltests.Options().with_scrubber(
            approvaltests.scrubbers.combine_scrubbers(
                PATH_SCRUBBER, WARNING_COUNT_SCRUBBER
            )
        ),
    )


class TestClangTidyExecutor:
    """Test of ClangTidyExecutor class."""

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_no_error(
        self, default_config: Config, sample_proj_no_error: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in no error."""

        config = copy.deepcopy(default_config)
        config.build_dir = str(sample_proj_no_error / "build")
        input_file = str(sample_proj_no_error / "src" / "sample_function.cpp")

        async with ClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_warning(
        self, default_config: Config, sample_proj_warning: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in a warning."""

        config = copy.deepcopy(default_config)
        config.build_dir = str(sample_proj_warning / "build")
        input_file = str(sample_proj_warning / "src" / "sample_function.cpp")

        async with ClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_error(
        self, default_config: Config, sample_proj_error: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in an error."""

        config = copy.deepcopy(default_config)
        config.build_dir = str(sample_proj_error / "build")
        input_file = str(sample_proj_error / "src" / "sample_function.cpp")

        async with ClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)


class TestCachedClangTidyExecutor:
    """Test of CachedClangTidyExecutor class."""

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_no_error(
        self, default_config_with_cache: Config, sample_proj_no_error: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in no error."""

        config = copy.deepcopy(default_config_with_cache)
        config.build_dir = str(sample_proj_no_error / "build")
        input_file = str(sample_proj_no_error / "src" / "sample_function.cpp")

        async with CachedClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_warning(
        self, default_config_with_cache: Config, sample_proj_warning: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in a warning."""

        config = copy.deepcopy(default_config_with_cache)
        config.build_dir = str(sample_proj_warning / "build")
        input_file = str(sample_proj_warning / "src" / "sample_function.cpp")

        async with CachedClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)

    @pytest.mark.asyncio
    async def test_execute_clang_tidy_error(
        self, default_config_with_cache: Config, sample_proj_error: pathlib.Path
    ):
        """Test of execute_clang_tidy resulting in an error."""

        config = copy.deepcopy(default_config_with_cache)
        config.build_dir = str(sample_proj_error / "build")
        input_file = str(sample_proj_error / "src" / "sample_function.cpp")

        async with CachedClangTidyExecutor(config=config) as executor:
            result = await executor.execute(input_file=input_file)

        check_result(input_file, result)
