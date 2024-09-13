from logging import getLogger
from uuid import UUID
from models.users import UserORM
from schemas.users import SUser
from utils.absract.service import BaseService
from aiogram.types.user import User

logger = getLogger(__name__)

class UserService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)

    
    async def check_user(self, user: User) -> None:
        async with self.uow:
            user_data: dict = user.model_dump(mode="python")
            user_data.update({
                    "tgid": user_data.pop("id")
                })
            user_data: dict = SUser(**user_data).model_dump(mode="python")
            user_model: UserORM = await self.uow.users.get_by_tgid(user.id)
            if isinstance(user_model, UserORM):
                user_data.update({
                    "id": user_model.id
                })
                id: UUID = user_data.pop('id')
                user_data.pop('tgid')
                await self.uow.users.update(user_data, id)
            else:
                await self.uow.users.add_one(user_data)
            await self.uow.commit(True)