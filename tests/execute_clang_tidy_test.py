"""Test of execute_clang_tidy.py.
"""

import copy
import pathlib

import approvaltests
import approvaltests.scrubbers
import trio
import trio.testing

from clang_tidy_checker.config import Config
from clang_tidy_checker.execute_clang_tidy import execute_clang_tidy, ExecutionResult

from .path_scrubber import PATH_SCRUBBER
from .warning_count_scrubber import WARNING_COUNT_SCRUBBER


def check_result(result: ExecutionResult):
    """Check a result.

    Args:
        result (ExecutionResult): Result.
    """

    approvaltests.approvals.verify(
        f"""input_file: {result.input_file}
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


@trio.testing.trio_test
async def test_execute_clang_tidy_no_error(
    default_config: Config, sample_proj_no_error: pathlib.Path
):
    """Test of execute_clang_tidy resulting in no error."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_no_error / "build")
    input_file = str(sample_proj_no_error / "src" / "sample_function.cpp")

    result = await execute_clang_tidy(config=config, input_file=input_file)

    check_result(result)


@trio.testing.trio_test
async def test_execute_clang_tidy_warning(
    default_config: Config, sample_proj_warning: pathlib.Path
):
    """Test of execute_clang_tidy resulting in a warning."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_warning / "build")
    input_file = str(sample_proj_warning / "src" / "sample_function.cpp")

    result = await execute_clang_tidy(config=config, input_file=input_file)

    check_result(result)


@trio.testing.trio_test
async def test_execute_clang_tidy_error(
    default_config: Config, sample_proj_error: pathlib.Path
):
    """Test of execute_clang_tidy resulting in an error."""

    config = copy.deepcopy(default_config)
    config.build_dir = str(sample_proj_error / "build")
    input_file = str(sample_proj_error / "src" / "sample_function.cpp")

    result = await execute_clang_tidy(config=config, input_file=input_file)

    check_result(result)
