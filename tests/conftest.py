"""Configuration of pytest.
"""

import pathlib
import subprocess

import pytest
import trio

from clang_tidy_checker.config import Config, parse_config_from_dict

THIS_DIR = pathlib.Path(__file__).absolute().parent
SAMPLE_DIR = THIS_DIR.parent / "sample_inputs"


def _configure_source(source_dir: pathlib.Path):
    """Configure a source directory.

    Args:
        source_dir (pathlib.Path): Source directory.
    """

    build_dir = source_dir / "build"
    if not build_dir.exists():
        build_dir.mkdir()
    subprocess.run(
        ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE", ".."],
        cwd=str(build_dir),
        check=True,
    )


@pytest.fixture(scope="session")
def sample_proj_no_error() -> pathlib.Path:
    """Fixture to configure sample proj_no_error.

    Returns:
        pathlib.Path: Source directory.
    """

    source_dir = SAMPLE_DIR / "proj_no_error"
    _configure_source(source_dir)

    return source_dir


@pytest.fixture(scope="session")
def default_config() -> Config:
    """Fixture of default configuration.

    Returns:
        Config: Default configuration.
    """

    return trio.run(parse_config_from_dict, {})
