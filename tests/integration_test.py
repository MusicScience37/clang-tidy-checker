"""Integration tests."""

import pathlib
import typing

import approvaltests
import trio
import trio.testing

from .path_scrubber import PATH_SCRUBBER


async def execute(command: typing.List[str], *, cwd: str) -> None:
    """Execute a command."""

    result = await trio.run_process(
        command,
        cwd=cwd,
        check=False,
        capture_stdout=True,
        capture_stderr=True,
    )

    approvaltests.approvals.verify(
        f"""exit_code: {result.returncode}
stdout:
{result.stdout.decode("utf8")}
stderr:
{result.stderr.decode("utf8")}
""",
        options=approvaltests.Options().with_scrubber(PATH_SCRUBBER),
    )


@trio.testing.trio_test
async def test_check_proj_no_error(sample_proj_no_error: pathlib.Path):
    """Test of checking project without errors."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_no_error),
    )


@trio.testing.trio_test
async def test_check_proj_warning(sample_proj_warning: pathlib.Path):
    """Test of checking project with a warnings."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_warning),
    )


@trio.testing.trio_test
async def test_check_proj_error(sample_proj_error: pathlib.Path):
    """Test of checking project with an error."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_error),
    )
