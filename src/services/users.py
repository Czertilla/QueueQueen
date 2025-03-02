from logging import getLogger
from uuid import UUID
from models.users import UserORM
from schemas.users import SUser
from utils.abstract.service import BaseService
from aiogram.types.user import User

logger = getLogger(__name__)

class UserService(BaseService):
    async def check_username(self, value: str) -> bool:
        async with self.uow:
            self.uow.users.check_username(value)

    
    async def update_user(self, user: User) -> SUser:
        logger.debug(f"updating data for {user=}")
        async with self.uow:
            user_data: dict = user.model_dump()
            user_data.update({
                    "tgid": user_data.pop("id")
                })
            user_model = await self.uow.users.get_by_tgid(user.id)
            if isinstance(user_model, UserORM):
                logger.debug(f"data for {user=} already exists")
                user_data.update({"id": user_model.id})
                logger.debug(f"filtering unnecessary attributes for {user=}")
                user_data = SUser(**user_data).model_dump()
                await self.uow.users.update(user_data, user_model.id)
            else:
                logger.debug(f"data for {user=} not exists yet")
                user_model = await self.uow.users.add_n_return(user_data)
            response = SUser.model_validate(user_model)
            await self.uow.commit(True)
        logger.debug(f"after update {user=} got {response=}")
        return response