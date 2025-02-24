from abc import ABC, abstractmethod
from typing import Type

from repositories.queues import QueueRepo
from repositories.users import UserRepo


class ABCUnitOfWork(ABC):
    users: Type[UserRepo]
    queues: Type[QueueRepo]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
