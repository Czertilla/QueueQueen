from utils.absract.unit_of_work import ABCUnitOfWork


class BaseService:
    def __init__(self, uow: ABCUnitOfWork) -> None:
        self.uow = uow
