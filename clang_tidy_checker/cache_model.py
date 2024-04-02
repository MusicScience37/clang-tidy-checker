"""Model of cached results."""

import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# pylint: disable=too-few-public-methods


class ModelBase(DeclarativeBase):
    """Base class for ORM declarations."""


class CachedCheckResultModel(ModelBase):
    """Table of cached results."""

    __tablename__ = "cached_result"

    source_hash: Mapped[str] = mapped_column(String(100), primary_key=True)
    exit_code: Mapped[int]
    stdout: Mapped[str]
    stderr: Mapped[str]
    created_at: Mapped[datetime.datetime]
