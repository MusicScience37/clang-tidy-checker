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
async def test_help(sample_proj_no_error: pathlib.Path):
    """Test of help message."""

    await execute(
        ["clang-tidy-checker", "--help"],
        cwd=str(sample_proj_no_error),
    )


@trio.testing.trio_test
async def test_config(sample_proj_no_error: pathlib.Path):
    """Test of config option."""

    await execute(
        [
            "clang-tidy-checker",
            "--no-ascii",
            "--config",
            str(sample_proj_no_error.parent / "configs" / "main_only.yaml"),
        ],
        cwd=str(sample_proj_no_error),
    )


@trio.testing.trio_test
async def test_build_dir(sample_proj_no_error: pathlib.Path):
    """Test of build_dir option."""

    await execute(
        ["clang-tidy-checker", "--no-ascii", "--build_dir", "."],
        cwd=str(sample_proj_no_error),
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


@trio.testing.trio_test
async def test_extra_args(sample_proj_warning: pathlib.Path):
    """Test of extra arguments to clang-tidy."""

    await execute(
        [
            "clang-tidy-checker",
            "--no-ascii",
            "--extra_arg",
            "--extra-arg=-any",
        ],
        cwd=str(sample_proj_warning),
    )
