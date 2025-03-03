from database import new_session
from utils.abstract.unit_of_work import ABCUnitOfWork
from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

logger = getLogger(__name__)


class Count:
    """
    Simple counter class for demonstration purposes.
    """
    c = 0


class UnitOfWork(ABCUnitOfWork):
    """
    Implementation of the Unit of Work pattern using SQLAlchemy's AsyncSession.

    Manages database sessions and transactions.
    """

    def __init__(self):
        """
        Initializes the UnitOfWork with a new session factory.
        """
        self.new_session = new_session
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        """
        Enters the asynchronous context and creates a new database session.

        Returns:
            UnitOfWork: The UnitOfWork instance.
        """
        self.session = self.new_session()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """
        Exits the asynchronous context, rolling back the transaction and closing the session.

        Args:
            *args: Arguments passed from the context manager.
        """
        await self.rollback()
        if self.session:
            await self.session.close()
        self.session = None

    async def commit(self, flush: bool = False) -> None:
        """
        Commits the transaction.

        Args:
            flush: Whether to flush the session before committing.
        """
        if self.session:
            if flush:
                await self.session.flush()
            await self.session.commit()

    async def rollback(self) -> None:
        """
        Rolls back the transaction.
        """
        if self.session:
            await self.session.rollback()