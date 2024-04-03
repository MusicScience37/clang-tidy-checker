"""Tables of cached results."""

import datetime
import typing

import sqlalchemy
import sqlalchemy.orm

from clang_tidy_checker.cache_model import CachedCheckResultModel, ModelBase
from clang_tidy_checker.check_result import CheckResult


class CacheTable:
    """Tables of cached results."""

    def __init__(self, engine: sqlalchemy.Engine) -> None:
        self._engine = engine
        ModelBase.metadata.create_all(engine)

    def save(self, source_hash: str, result: CheckResult) -> None:
        """Save a result of a check."""
        with sqlalchemy.orm.Session(self._engine) as session:
            cached_result = CachedCheckResultModel(
                source_hash=source_hash,
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                created_at=datetime.datetime.now(),
            )
            session.add(cached_result)
            session.commit()

    def load(self, source_hash: str) -> typing.Optional[CheckResult]:
        """Load a cached result of a check.

        Args:
            source_hash (str): Hash of source code.

        Returns:
            typing.Optional[CheckResult]: Cached result if found.
        """
        with sqlalchemy.orm.Session(self._engine) as session:
            statement = sqlalchemy.select(CachedCheckResultModel).where(
                CachedCheckResultModel.source_hash == source_hash
            )
            cached_result = session.scalars(statement).one_or_none()
            if cached_result is None:
                return None
            return CheckResult(
                exit_code=cached_result.exit_code,
                stdout=cached_result.stdout,
                stderr=cached_result.stderr,
            )


def create_cache_table_at(filepath: str) -> CacheTable:
    """Create a table of caches at a file path.

    Args:
        filepath (str): File path.

    Returns:
        CacheTable: Created table.
    """
    return CacheTable(engine=sqlalchemy.create_engine(f"sqlite:///{filepath}"))
