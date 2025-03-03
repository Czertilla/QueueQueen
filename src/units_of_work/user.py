from repositories.users import UserRepo
from units_of_work._unit_of_work import UnitOfWork


class UserUOW(UnitOfWork):
    """
    A Unit of Work implementation that provides access to the User repository.

    Extends the base UnitOfWork and initializes the User repository.
    """

    async def __aenter__(self) -> "UserUOW":
        """
        Enters the asynchronous context, initializes the User repository, and returns the instance.

        Overrides the base class's __aenter__ method to set up the User repository.

        Returns:
            UserUOW: The UserUOW instance.
        """
        rtrn = await super().__aenter__()
        self.users = UserRepo(self.session)
        return rtrn
