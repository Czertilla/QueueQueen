from typing import AsyncGenerator
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import new_session, BaseRepo
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
    
    