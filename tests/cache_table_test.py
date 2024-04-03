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
        table = CacheTable(engine=engine_for_test)

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
        table = CacheTable(engine=engine_for_test)

        source_hash = "abc"
        loaded_result = table.load(source_hash=source_hash)

        assert loaded_result is None
