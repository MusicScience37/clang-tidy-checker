"""Test of cache_table.py."""

import pytest
import sqlalchemy

from clang_tidy_checker.cache_table import CacheTable
from clang_tidy_checker.check_result import CheckResult

# pylint: disable=redefined-outer-name


@pytest.fixture
def engine_for_test() -> sqlalchemy.Engine:
    """Engine of database for tests."""
    return sqlalchemy.create_engine("sqlite://")


class TestCacheTable:
    """Test of CacheTable class."""

    def test_save_result(self, engine_for_test: sqlalchemy.Engine) -> None:
        """Test to save a result."""
        table = CacheTable(engine=engine_for_test, max_cache_entries=100)

        source_hash = "abc"
        result = CheckResult(
            exit_code=12, stdout="Sample output.", stderr="Sample error."
        )

        table.save(source_hash=source_hash, result=result)

        loaded_result = table.load(source_hash=source_hash)

        assert loaded_result == result

    def test_try_to_get_non_existing_result(
        self, engine_for_test: sqlalchemy.Engine
    ) -> None:
        """Test to try to get a non-existing result."""
        table = CacheTable(engine=engine_for_test, max_cache_entries=100)

        source_hash = "abc"
        loaded_result = table.load(source_hash=source_hash)

        assert loaded_result is None

    def test_remove_old_data(self, engine_for_test: sqlalchemy.Engine) -> None:
        """Test to remove old data."""
        table = CacheTable(engine=engine_for_test, max_cache_entries=2)

        source_hash1 = "abc"
        result1 = CheckResult(
            exit_code=12, stdout="Sample output.", stderr="Sample error."
        )
        table.save(source_hash=source_hash1, result=result1)

        source_hash2 = "def"
        result2 = CheckResult(
            exit_code=34, stdout="Sample output 2.", stderr="Sample error 2."
        )
        table.save(source_hash=source_hash2, result=result2)

        source_hash3 = "ghi"
        result3 = CheckResult(
            exit_code=56, stdout="Sample output e.", stderr="Sample error 3."
        )
        table.save(source_hash=source_hash3, result=result3)

        assert table.load(source_hash=source_hash1) is None
        assert table.load(source_hash=source_hash2) == result2
        assert table.load(source_hash=source_hash3) == result3
