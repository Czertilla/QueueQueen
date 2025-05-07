from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import BaseRepo
from logging import getLogger

from models.users import UserORM as Model

logger = getLogger(__name__)


class UserRepo(BaseRepo[Model]):
    """
    Repository for managing UserORM entities.
    """

    model = Model

    async def check_username(self, value: str) -> bool:
        """
        Checks if a username exists in the database.

        Args:
            value: The username to check.

        Returns:
            True if the username exists, False otherwise.
        """
        user = (
            await self.execute(
                select(self.model).
                where(self.model.username == value)
            )
        ).scalar_one_or_none()
        return user is not None

    async def get_by_tgid(self, tgid: int) -> Model:
        """
        Retrieves a user by their Telegram ID.

        Args:
            tgid: The Telegram ID of the user.

        Returns:
            The UserORM object, or None if not found.
        """
        return (
            await self.execute(select(Model).where(Model.tgid == tgid))
        ).scalar_one_or_none()

    async def get_with_positions(self, id: UUID) -> Model | None:
        """
        Retrieves a user with their associated positions.

        Args:
            id: The UUID of the user.

        Returns:
            The UserORM object with positions, or None if not found.
        """
        return (
            await self.execute(
                select(self.model)
                .where(self.model.id == id)
                .options(selectinload(self.model.positions))
            )
        ).scalar_one_or_none()

    async def get_by_username(self, username: str) -> Model:
        """
        Retrieves a user by their Telegram username.

        Args:
            username (str): The Telegram username without `@` of user

        Returns:
            model: The UserORM object, or None if not found.
        """
        logger.debug(f"getting user by {username=}")
        return (
            await self.execute(
                select(Model).where(Model.username == username)
            )
        ).scalar_one_or_none()
