from logging import getLogger
from uuid import UUID
from models.users import UserORM
from aiogram.types.user import User
from schemas.users import SUser
from utils.absract.service import BaseService

logger = getLogger(__name__)

class QueueService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)


    async def check_user(self, user: User):
        async with self.uow:
            user_data: dict = user.model_dump(mode="python")
            user_data.update({
                    "tgid": user_data.pop("id")
                })
            user_model: UserORM = await self.uow.users.get_by_tgid(user.id)
            if isinstance(user_model, UserORM):
                user_data.update({
                    "id": user_model.id
                })
                await self.uow.users.update(user_data)
            else:
                await self.uow.users.add_one(user_data)