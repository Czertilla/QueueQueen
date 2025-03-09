from logging import getLogger
from uuid import UUID, uuid1
from models.users import UserORM
from schemas.users import SUser
from utils.abstract.service import BaseService
from aiogram.types.user import User

logger = getLogger(__name__)


class UserService(BaseService):
    """
    Service class for managing user-related operations.

    Provides methods for checking usernames and updating user information.
    """

    async def check_username(self, value: str) -> bool:
        """
        Checks if a username exists.

        Args:
            value: The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        async with self.uow:
            return await self.uow.users.check_username(value)

    @staticmethod    
    def filt_user_data(user_data: dict) -> dict:
        logger.debug(f"filtering unnecessary attributes for {user_data=}")
        if f := 'id' not in user_data:
            user_data['id'] = uuid1()
        user_data = SUser(**user_data).model_dump()
        if f:
            user_data.pop('id')
        return user_data

    async def update_user(self, user: User) -> SUser:
        """
        Updates or creates a user based on the provided aiogram User object.

        Args:
            user: The aiogram User object.

        Returns:
            SUser: The updated or created user as an SUser schema.
        """
        response: SUser
        logger.debug(f"updating data for {user=}")
        async with self.uow:
            user_data: dict = user.model_dump()
            user_data.update({"tgid": user_data.pop("id")})
            user_model = await self.uow.users.get_by_tgid(user.id)
            if isinstance(user_model, UserORM):
                logger.debug(f"data for {user=} already exists")
                user_data.update({"id": user_model.id})
                user_data = self.filt_user_data(user_data)
                await self.uow.users.update(user_data, user_model.id)
            else:
                logger.debug(f"data for {user=} not exists yet")
                user_data = self.filt_user_data(user_data)
                user_model = await self.uow.users.add_n_return(user_data)
            response = SUser.model_validate(user_model)
            await self.uow.commit(True)
        logger.debug(f"after update {user=} got {response=}")
        return response
