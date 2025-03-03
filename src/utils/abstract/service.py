from utils.abstract.unit_of_work import ABCUnitOfWork


class BaseService:
    """
    Base service class for application services.

    Provides a common interface for services that require a Unit of Work.

    Attributes:
        uow (ABCUnitOfWork): The Unit of Work instance used by the service.
    """

    def __init__(self, uow: ABCUnitOfWork) -> None:
        """
        Initializes the BaseService with a Unit of Work.

        Args:
            uow (ABCUnitOfWork): The Unit of Work instance.
        """
        self.uow = uow