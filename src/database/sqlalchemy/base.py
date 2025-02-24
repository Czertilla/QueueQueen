from logging import getLogger, Logger
from typing import Any
from uuid import uuid4, UUID
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import Result, delete, insert, select, update
from utils.abstract.repository import AbstractRepository


class IdMixin:
    """Mixin class to provide a UUID primary key for database models."""

    @declared_attr
    def id(cls) -> Mapped[UUID]:
        """Defines the primary key field as a UUID."""
        return mapped_column(primary_key=True, default=uuid4)


class Base(DeclarativeBase, IdMixin):
    """Abstract base class for SQLAlchemy models, including default type 
    mappings."""

    __abstract__ = True

    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime: DateTime(timezone=True)
    }


class SQLAlchemyRepository(AbstractRepository):
    """Asynchronous repository class for handling database operations using 
    SQLAlchemy."""

    model = Base
    logger: Logger

    def __new__(cls, *args: Any, **kwargs: Any) -> "SQLAlchemyRepository":
        """Creates a new instance and initializes the logger if it is not 
        already set."""
        if not hasattr(cls, "logger"):
            cls.logger = getLogger(f"SQL.{cls.__name__}")
        return super().__new__(cls)

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the repository with an async database session.

        :param session: The SQLAlchemy async session instance.
        """
        super().__init__()
        self.session: AsyncSession = session

    async def execute(self, stmt: Any, flush: bool = False) -> Result:
        """
        Executes a given SQLAlchemy statement asynchronously.

        :param stmt: The SQL statement to execute.
        :param flush: Whether to flush the session after execution.
        :return: The execution result.
        """
        self.logger.debug(stmt)
        result: Result = await self.session.execute(statement=stmt)
        if flush:
            await self.session.flush()
        return result

    async def flush(self) -> None:
        """Flushes the current database session."""
        await self.session.flush()

    async def get(self, id: UUID) -> Base | None:
        """
        Retrieves a model instance by its ID.

        :param id: The UUID of the instance.
        :return: The instance if found, else None.
        """
        return await self.session.get(self.model, id)

    async def get_with_options(self, id: UUID, options: tuple) -> Base | None:
        """
        Retrieves a model instance by its ID with additional query options.

        :param id: The UUID of the instance.
        :param options: SQLAlchemy options to apply to the query.
        :return: The instance if found, else None.
        """
        stmt = select(self.model).where(self.model.id == id).options(*options)
        return (await self.execute(stmt)).unique().scalar_one_or_none()

    async def merge(self, data_orm: Base, flush: bool = False) -> None:
        """
        Merges an instance into the session.

        :param data_orm: The ORM instance to merge.
        :param flush: Whether to flush the session after merging.
        """
        await self.session.merge(data_orm)
        if flush:
            await self.session.flush()

    async def add_one(self, data: dict[str, Any]) -> UUID:
        """
        Inserts a new instance into the database and returns its ID.

        :param data: The data dictionary for the new instance.
        :return: The UUID of the created instance.
        """
        stmt = insert(self.model).values(**data).returning(self.model.id)
        return (await self.execute(stmt, flush=False)).scalar_one()

    async def add_n_return(
            self, data: dict[str, Any], options: tuple = ()
    ) -> Base:
        """
        Inserts a new instance and returns the full instance.

        :param data: The data dictionary for the new instance.
        :param options: SQLAlchemy options to apply.
        :return: The created instance.
        """
        stmt = insert(self.model).values(
            **data).returning(self.model).options(*options)
        return (await self.execute(stmt, flush=False)).scalar_one()

    async def update(self, data: dict[str, Any], id: UUID) -> Result:
        """
        Updates an instance in the database.

        :param data: The data dictionary with updated values.
        :param id: The UUID of the instance to update.
        :return: The execution result.
        """
        stmt = update(self.model).where(self.model.id == id).values(**data)
        return await self.execute(stmt)

    async def find_by_id(self, id: UUID) -> Base | None:
        """
        Finds an instance by its ID.

        :param id: The UUID of the instance.
        :return: The instance if found, else None.
        """
        stmt = select(self.model).where(self.model.id == id)
        return (await self.execute(stmt)).scalar_one_or_none()

    async def find_all(self, **filters: Any) -> list[Base]:
        """
        Finds all instances matching given filters.

        :param filters: Key-value pairs to filter results.
        :return: A list of matching instances.
        """
        stmt = select(self.model).filter_by(**filters)
        result = await self.execute(stmt)
        return result.scalars().all()

    async def check_existence(self, id: UUID) -> bool:
        """
        Checks whether an instance with the given ID exists.

        :param id: The UUID of the instance.
        :return: True if it exists, otherwise False.
        """
        return (await self.find_by_id(id)) is not None

    async def delete(self, id: UUID) -> None:
        """
        Deletes an instance from the database.

        :param id: The UUID of the instance to delete.
        """
        await self.execute(delete(self.model).where(self.model.id == id))
