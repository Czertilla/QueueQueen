from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from database import BaseRepo
from models.positions import PositionORM
from models.queues import QueueORM


class QueueRepo(BaseRepo):
    """
    Repository class for handling queue-related database operations.
    """

    model = QueueORM

    async def get_by_chat_id(self, chat_id: int) -> model | None:
        """
        Retrieves a queue by its chat ID.

        :param chat_id: The chat ID associated with the queue.
        :return: The queue instance if found, otherwise None.
        """
        self.logger.debug(f"Fetching queue by chat_id={chat_id}")
        result = await self.execute(
            select(self.model)
            .where(self.model.chat_id == chat_id)
        )
        queue = result.scalar_one_or_none()
        self.logger.debug(f"Queue found: {queue}")
        return queue

    async def get_with_positions(self, id: UUID) -> model | None:
        """
        Retrieves a queue with its positions preloaded.

        :param id: The UUID of the queue.
        :return: The queue instance with positions if found, otherwise None.
        """
        self.logger.debug(f"Fetching queue with positions by id={id}")
        result = await self.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.positions).joinedload(PositionORM.user)
            )
        )
        queue = result.scalar_one_or_none()
        self.logger.debug(f"Queue with positions: {queue}")
        return queue

    async def get_position(
            self, queue_id: UUID, user_id: UUID
    ) -> PositionORM | None:
        """
        Retrieves a position in a queue for a specific user.

        :param queue_id: The UUID of the queue.
        :param user_id: The UUID of the user.
        :return: The position instance if found, otherwise None.
        """
        self.logger.debug(f"Fetching position in {queue_id=} for {user_id=}")
        result = await self.execute(
            select(PositionORM)
            .where(PositionORM.queue_id == queue_id)
            .where(PositionORM.user_id == user_id)
        )
        position = result.scalar_one_or_none()
        self.logger.debug(f"Position found: {position}")
        return position

    async def add_position(self, queue: model, user_id: UUID) -> int:
        """
        Adds a user to the queue if they are not already in it.

        :param queue: The queue instance.
        :param user_id: The UUID of the user.
        :return: The position of the user in the queue, or -1 if they are 
            already in it.
        """
        self.logger.debug(f"Adding {user_id=} to {queue.id=}")

        if await self.get_position(queue.id, user_id):
            self.logger.debug(f"User {user_id} is already in queue {queue.id}")
            return -1

        new_position = len(queue.positions)
        queue.positions.append(PositionORM(
            queue_id=queue.id, user_id=user_id, position=new_position))

        self.logger.debug(
            f"User {user_id} added to queue {queue.id} at {new_position=}")
        return new_position

    async def remove_position(
            self, queue: model, user_id: UUID
    ) -> tuple[bool, int | None]:
        """
        Removes a user's position from the queue.

        :param queue: The queue instance.
        :param user_id: The UUID of the user whose position should be removed.
        :return: A tuple containing:
            - A boolean indicating whether the removal was successful.
            - The Telegram ID of the next user in line if applicable, 
                otherwise None.
        """
        self.logger.debug(
            f"Removing position for user_id={user_id} in queue_id={queue.id}")
        target = await self.get_position(queue.id, user_id)

        if not target:
            self.logger.info(
                f"User {user_id} not found in queue {queue.id}")
            return False, None

        next_user_id = queue.positions[1].user.tgid if len(
            queue.positions) > 1 and target.position == 0 else None
        answer = (True, next_user_id)

        await self.execute(
            delete(PositionORM)
            .where(PositionORM.queue_id == queue.id)
            .where(PositionORM.user_id == user_id)
        )

        queue.positions.sort(key=lambda pos: pos.created_at)

        for p, position in enumerate(queue.positions):
            position.position = p

        self.logger.debug(
            f"User {user_id} removed from queue {queue.id}. {next_user_id=}")
        return answer

    async def clear(self, queue_id: UUID) -> None:
        """
        Clears all positions from a queue.

        :param queue_id: The UUID of the queue to be cleared.
        """
        self.logger.debug(f"Clearing queue with queue_id={queue_id}")
        await self.execute(
            delete(PositionORM).where(PositionORM.queue_id == queue_id)
        )
        self.logger.debug(f"Queue {queue_id} has been cleared")
