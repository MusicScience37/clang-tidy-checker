"""Test of search_clang_tidy.py
"""

import pathlib
import shutil

import pytest

from clang_tidy_checker.search_clang_tidy import search_clang_tidy


@pytest.mark.asyncio
async def test_search_clang_tidy_with_name():
    """Test of search_clang_tidy with executable name."""

    path = await search_clang_tidy("clang-tidy")

    assert "clang-tidy" in path
    assert not pathlib.Path(path).is_symlink()
    assert pathlib.Path(path).is_file()


@pytest.mark.asyncio
async def test_search_clang_tidy_with_path():
    """Test of search_clang_tidy with executable name."""

    input_path = shutil.which("clang-tidy")

    path = await search_clang_tidy(input_path)

    assert "clang-tidy" in path
    assert not pathlib.Path(path).is_symlink()
    assert pathlib.Path(path).is_file()


@pytest.mark.asyncio
async def test_search_clang_tidy_not_found():
    """Test of search_clang_tidy with an executable name not found."""

    with pytest.raises(RuntimeError):
        await search_clang_tidy("invalid-command")
