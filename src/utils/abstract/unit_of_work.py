from abc import ABC, abstractmethod
from typing import Type

from repositories.queues import QueueRepo
from repositories.users import UserRepo


class ABCUnitOfWork(ABC):
    """
    Abstract base class for Unit of Work implementations.

    Defines the interface for managing repositories and transactions.

    Attributes:
        users (Type[UserRepo]): The repository class for user-related operations.
        queues (Type[QueueRepo]): The repository class for queue-related operations.
    """

    users: Type[UserRepo]
    queues: Type[QueueRepo]

    @abstractmethod
    def __init__(self):
        """
        Initializes the Unit of Work.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        """
        Enters the asynchronous context.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        """
        Exits the asynchronous context.

        Args:
            *args: Arguments passed from the context manager.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        """
        Commits the transaction.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        """
        Rolls back the transaction.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError