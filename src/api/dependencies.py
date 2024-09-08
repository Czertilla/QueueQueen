from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends
from units_of_work.all import AllUOW
from units_of_work.user import UserUOW
from utils.absract.unit_of_work import ABCUnitOfWork


RoleUUID = Annotated[UUID, Cookie()]

UsersUOWDep = Annotated[ABCUnitOfWork, Depends(UserUOW)]
ALLUOWDep = Annotated[ABCUnitOfWork, Depends(AllUOW)]