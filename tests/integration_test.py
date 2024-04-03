"""Integration tests."""

import pathlib
import subprocess
import typing

import approvaltests
import pytest

from .path_scrubber import PATH_SCRUBBER
from .warning_count_scrubber import WARNING_COUNT_SCRUBBER

THIS_DIR = pathlib.Path(__file__).absolute().parent


async def execute(command: typing.List[str], *, cwd: str, repeat: bool = False) -> None:
    """Execute a command."""

    repetitions = 1
    if repeat:
        repetitions = 3

    for _ in range(repetitions):
        result = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    approvaltests.approvals.verify(
        f"""exit_code: {result.returncode}
stdout:
{result.stdout.decode("utf8")}
stderr:
{result.stderr.decode("utf8")}
""",
        options=approvaltests.Options().with_scrubber(
            approvaltests.scrubbers.combine_scrubbers(
                PATH_SCRUBBER, WARNING_COUNT_SCRUBBER
            )
        ),
    )


@pytest.mark.asyncio
async def test_help(sample_proj_no_error: pathlib.Path):
    """Test of help message."""

    await execute(
        ["clang-tidy-checker", "--help"],
        cwd=str(sample_proj_no_error),
    )


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_build_dir(sample_proj_no_error: pathlib.Path):
    """Test of build_dir option."""

    await execute(
        ["clang-tidy-checker", "--no-ascii", "--build_dir", "."],
        cwd=str(sample_proj_no_error),
    )


@pytest.mark.asyncio
async def test_check_proj_no_error(sample_proj_no_error: pathlib.Path):
    """Test of checking project without errors."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_no_error),
    )


@pytest.mark.asyncio
async def test_check_proj_warning(sample_proj_warning: pathlib.Path):
    """Test of checking project with a warnings."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_warning),
    )


@pytest.mark.asyncio
async def test_check_proj_error(sample_proj_error: pathlib.Path):
    """Test of checking project with an error."""

    await execute(
        ["clang-tidy-checker", "--no-ascii"],
        cwd=str(sample_proj_error),
    )


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_cache_dir(sample_proj_warning: pathlib.Path):
    """Test of cache directory."""

    await execute(
        [
            "clang-tidy-checker",
            "--no-ascii",
            "--cache_dir",
            str(THIS_DIR.parent / ".clang-tidy-cache"),
        ],
        cwd=str(sample_proj_warning),
        repeat=True,
    )
