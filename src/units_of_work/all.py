from repositories.queues import QueueRepo
from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork


class AllUOW(UnitOfWork):
    """
    A specific Unit of Work implementation that provides access to all repositories.

    Extends the base UnitOfWork and initializes repositories for users and queues.
    """

    async def __aenter__(self) -> "AllUOW":
        """
        Enters the asynchronous context, initializes repositories, and returns the instance.

        Overrides the base class's __aenter__ method to set up repositories.

        Returns:
            AllUOW: The AllUOW instance.
        """
        rtrn = await super().__aenter__()

        self.users = UserRepo(self.session)
        self.queues = QueueRepo(self.session)

        return rtrn