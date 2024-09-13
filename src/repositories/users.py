from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import BaseRepo
from logging import getLogger

from models.users import UserORM

logger = getLogger(__name__)

class UserRepo(BaseRepo):
    model = UserORM

    async def check_username(self, value) -> bool:
        user = (
            await self.execute(
                select(UserORM).
                where(UserORM.username == value)
            )
        ).scalar_one_or_none()
        return user is not None


    async def get_by_tgid(self, tgid: int) -> model:
        return (
            await self.execute(
                select(UserORM)
                .where(UserORM.tgid == tgid)
            )
        ).scalar_one_or_none()
    

    async def get_with_positions(self, id: UUID) -> model|None:
         return (
            await self.execute(
                select(self.model)
                .where(self.model.id == id)
                .options(selectinload(self.model.positions))
            )
        ).scalar_one_or_none()
    