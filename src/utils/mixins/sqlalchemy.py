from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class TimestampMixin:
    """
    Mixin class that adds timestamp columns to SQLAlchemy models.

    Provides `created_at` and `edited_at` columns for tracking record creation and modification times.
    """

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """
        Column representing the creation timestamp.

        Returns:
            Mapped[datetime]: A SQLAlchemy mapped column representing the creation timestamp.
        """
        return mapped_column(default=func.now())

    @declared_attr
    def edited_at(cls) -> Mapped[datetime | None]:
        """
        Column representing the last modification timestamp.

        Returns:
            Mapped[datetime | None]: A SQLAlchemy mapped column representing the modification timestamp,
                                       or None if the record has not been modified.
        """
        return mapped_column(onupdate=func.now())