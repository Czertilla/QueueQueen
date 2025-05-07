from logging import getLogger, Logger
from typing import Any, Generic, TypeVar
from uuid import uuid4, UUID
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import Result, delete, insert, select, update
from utils.abstract.repository import AbstractRepository


class IdMixin:
    """
    Mixin class that provides a UUID primary key for database models.
    """

    @declared_attr
    def id(cls) -> Mapped[UUID]:
        """
        Defines the primary key field as a UUID.

        Returns:
            Mapped[UUID]: A mapped column with a UUID primary key.
        """
        return mapped_column(primary_key=True, default=uuid4)


class Base(DeclarativeBase, IdMixin):
    """
    Abstract base class for SQLAlchemy models, including default type mappings.

    Attributes:
        type_annotation_map (dict): Maps Python types to SQLAlchemy types.
    """

    __abstract__ = True

    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime: DateTime(timezone=True)
    }

Model = TypeVar("Model", bound=type[Base])

class SQLAlchemyRepository(Generic[Model], AbstractRepository):
    """
    Asynchronous repository for performing database operations using SQLAlchemy.

    Attributes:
        model (type[Base]): The SQLAlchemy model class.
        logger (Logger): Logger instance for logging SQL operations.
    """

    model: type[Model]
    logger: Logger

    def __new__(cls, *args: Any, **kwargs: Any) -> "SQLAlchemyRepository":
        """
        Creates a new repository instance and initializes the logger.

        Returns:
            SQLAlchemyRepository: A new repository instance.
        """
        if not hasattr(cls, "logger"):
            cls.logger = getLogger(f"SQL.{cls.__name__}")
        return super().__new__(cls)

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the repository with an async SQLAlchemy session.

        Args:
            session (AsyncSession): The SQLAlchemy async session instance.
        """
        super().__init__()
        self.session: AsyncSession = session

    async def execute(self, stmt: Any, flush: bool = False) -> Result:
        """
        Executes a given SQLAlchemy statement asynchronously.

        Args:
            stmt (Any): The SQL statement to execute.
            flush (bool, optional): Whether to flush the session after
                execution. Defaults to False.

        Returns:
            Result: The execution result.
        """
        self.logger.debug(stmt)
        result: Result = await self.session.execute(statement=stmt)
        if flush:
            await self.session.flush()
        return result

    async def flush(self) -> None:
        """
        Flushes the current session, synchronizing it with the database.
        """
        await self.session.flush()

    async def get(self, id: UUID) -> Model | None:
        """
        Retrieves a model instance by its primary key.

        Args:
            id (UUID): The primary key of the instance.

        Returns:
            Model | None: The instance if found, otherwise None.
        """
        return await self.session.get(self.model, id)

    async def get_with_options(self, id: UUID, options: tuple) -> Model | None:
        """
        Retrieves a model instance by its primary key with additional query
            options.

        Args:
            id (UUID): The primary key of the instance.
            options (tuple): SQLAlchemy query options.

        Returns:
            model | None: The instance if found, otherwise None.
        """
        stmt = select(self.model).where(self.model.id == id).options(*options)
        return (await self.execute(stmt)).unique().scalar_one_or_none()

    async def merge(self, data_orm: Model, flush: bool = False) -> None:
        """
        Merges an instance into the session.

        Args:
            data_orm (Model): The ORM instance to merge.
            flush (bool, optional): Whether to flush the session after merging.
                Defaults to False.
        """
        await self.session.merge(data_orm)
        if flush:
            await self.session.flush()

    async def add_one(self, data: dict[str, Any]) -> UUID:
        """
        Inserts a new instance into the database and returns its primary key.

        Args:
            data (dict[str, Any]): The data dictionary for the new instance.

        Returns:
            UUID: The primary key of the created instance.
        """
        stmt = insert(self.model).values(**data).returning(self.model.id)
        return (await self.execute(stmt, flush=False)).scalar_one()

    async def add_n_return(
            self, data: dict[str, Any], options: tuple = ()
    ) -> Model:
        """
        Inserts a new instance and returns the full model instance.

        Args:
            data (dict[str, Any]): The data dictionary for the new instance.
            options (tuple, optional): SQLAlchemy query options. Defaults to ().

        Returns:
            Model: The created instance.
        """
        stmt = insert(self.model).values(
            **data).returning(self.model).options(*options)
        return (await self.execute(stmt, flush=False)).scalar_one()

    async def update(self, data: dict[str, Any], id: UUID) -> Result:
        """
        Updates an existing instance in the database.

        Args:
            data (dict[str, Any]): The updated data.
            id (UUID): The primary key of the instance to update.

        Returns:
            Result: The execution result.
        """
        stmt = update(self.model).where(self.model.id == id).values(**data)
        return await self.execute(stmt)

    async def find_by_id(self, id: UUID) -> Model | None:
        """
        Finds an instance by its primary key.

        Args:
            id (UUID): The primary key of the instance.

        Returns:
            Model | None: The instance if found, otherwise None.
        """
        stmt = select(self.model).where(self.model.id == id)
        return (await self.execute(stmt)).scalar_one_or_none()

    async def find_all(self, **filters: Any) -> list[Model]:
        """
        Finds all instances that match the given filters.

        Args:
            **filters (Any): Key-value pairs used to filter results.

        Returns:
            list[Model]: A list of matching instances.
        """
        stmt = select(self.model).filter_by(**filters)
        result = await self.execute(stmt)
        return result.scalars().all()

    async def check_existence(self, id: UUID) -> bool:
        """
        Checks if an instance with the given primary key exists.

        Args:
            id (UUID): The primary key of the instance.

        Returns:
            bool: True if the instance exists, otherwise False.
        """
        return (await self.find_by_id(id)) is not None

    async def delete(self, id: UUID) -> None:
        """
        Deletes an instance from the database.

        Args:
            id (UUID): The primary key of the instance to delete.
        """
        await self.execute(delete(self.model).where(self.model.id == id))
