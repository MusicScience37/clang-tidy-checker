"""Tables of cached results."""

import datetime
import typing

import sqlalchemy
import sqlalchemy.orm

from clang_tidy_checker.cache_model import CachedCheckResultModel, ModelBase
from clang_tidy_checker.check_result import CheckResult


class CacheTable:
    """Tables of cached results."""

    def __init__(self, engine: sqlalchemy.Engine, max_cache_entries: int) -> None:
        self._engine = engine
        ModelBase.metadata.create_all(engine)
        self._max_cache_entries = max_cache_entries

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

        self._remove_old_entries()

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

    def _remove_old_entries(self) -> None:
        """Remove old entries."""
        with sqlalchemy.orm.Session(self._engine) as session:
            current_num_entries = typing.cast(
                int,
                session.scalar(
                    sqlalchemy.select(
                        # Pylint wrongly generate an error.
                        # pylint: disable=not-callable
                        sqlalchemy.func.count(CachedCheckResultModel.source_hash)
                    )
                ),
            )
            if current_num_entries <= self._max_cache_entries:
                return
            removed_entries = current_num_entries - self._max_cache_entries
            statement = (
                sqlalchemy.select(CachedCheckResultModel)
                .order_by(CachedCheckResultModel.created_at.asc())
                .limit(removed_entries)
            )
            for entry in session.scalars(statement):
                session.delete(entry)
            session.commit()


def create_cache_table_at(filepath: str, max_cache_entries: int) -> CacheTable:
    """Create a table of caches at a file path.

    Args:
        filepath (str): File path.
        max_cache_entries (int): Maximum number of entries in the cache.

    Returns:
        CacheTable: Created table.
    """
    return CacheTable(
        engine=sqlalchemy.create_engine(f"sqlite:///{filepath}"),
        max_cache_entries=max_cache_entries,
    )
