"""Test of search_clang_tidy.py
"""

import shutil
import trio
import trio.testing

from clang_tidy_checker.search_clang_tidy import search_clang_tidy


@trio.testing.trio_test
async def test_search_clang_tidy_with_name():
    """Test of search_clang_tidy with executable name."""

    path = await search_clang_tidy("clang-tidy")

    assert "clang-tidy" in path
    assert not await trio.Path(path).is_symlink()
    assert await trio.Path(path).is_file()


@trio.testing.trio_test
async def test_search_clang_tidy_with_path():
    """Test of search_clang_tidy with executable name."""

    input_path = shutil.which("clang-tidy")

    path = await search_clang_tidy(input_path)

    assert "clang-tidy" in path
    assert not await trio.Path(path).is_symlink()
    assert await trio.Path(path).is_file()
