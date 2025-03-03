from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    """
    Abstract base class for repository implementations.

    Defines the interface for common data access operations.
    """

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Any:
        """
        Adds a single entity to the repository.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            The added entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def add_n_return(self, *args: Any, **kwargs: Any) -> Any:
        """
        Adds multiple entities to the repository and returns the result.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            The result of the add operation.
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: Any) -> Any | None:
        """
        Finds an entity by its ID.

        Args:
            id: The ID of the entity.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            The found entity, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def check_existence(self, *args: Any, **kwargs: Any) -> bool:
        """
        Checks if an entity exists based on given criteria.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            True if the entity exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def merge(self, *args: Any, **kwargs: Any) -> Any:
        """
        Merges an entity with existing data.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        Returns:
            The merged entity.
        """
        raise NotImplementedError
