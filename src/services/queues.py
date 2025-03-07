from logging import getLogger
from uuid import UUID
from models.positions import PositionORM
from models.queues import QueueORM
from models.users import UserORM
from aiogram.types.user import User
from schemas.queues import SAddUserResponse, SQueueList, SRemoveUserResponse
from schemas.users import SUser
from utils.abstract.service import BaseService

logger = getLogger(__name__)


class QueueService(BaseService):
    """
    Service class for managing queue-related operations.

    Provides methods for retrieving queue lists, adding users to queues,
    removing users from queues, and clearing queues.
    """

    async def get_queue_list(
            self, chat_id: int, from_admin: bool = False
    ) -> SQueueList:
        """
        Retrieves the queue list for a given chat.

        Args:
            chat_id (int): The ID of the chat.
            from_admin (bool): Whether the request is from an admin.
                Defaults to `False`

        Returns:
            SQueueList: The queue list.
        """
        response: SQueueList
        logger.info(f"constructing queue list for {chat_id=}")
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                logger.debug(f"{queue.id=} exists")
                queue_data: QueueORM = (
                    await self.uow.queues.get_with_positions(queue.id))
                assert isinstance(queue_data, QueueORM)
                logger.debug("sorting positions by timestamps")
                positions: list[SUser] = [
                    SUser.model_validate(pos.user) for pos in sorted(
                        queue_data.positions, key=lambda pos: pos.created_at
                    )]
                logger.debug(f"{len(positions)} positions retrieved ad sorted")
                response = SQueueList(id=queue_data.id, positions=positions)
            elif from_admin:
                logger.debug(
                    f"queue for {chat_id=} not exists, creating by admin")
                queue_id = await self.uow.queues.add_one({"chat_id": chat_id})
                if isinstance(queue_id, UUID):
                    logger.info(f"new {queue_id=} created for {chat_id=}")
                    response = SQueueList(
                        id=queue_id, positions=[], is_new=True)
                else:
                    logger.warning(
                        "some problem during attemp to crete queue for " +
                        f"{chat_id=}")
                    response = SQueueList(id=None, positions=None, is_new=True)
            else:
                logger.debug("queue for {chat_id=} not exists, no creating")
                response = SQueueList(id=None, positions=None, is_new=False)
            await self.uow.commit(True)
        logger.info(f"by args {chat_id=}, {from_admin=} got {response=}")
        return response

    async def add_user(self, user: SUser, chat_id: int) -> SAddUserResponse:
        """
        Adds a user to the queue.

        Args:
            user (SUser): The user to add.
            chat_id (int): The ID of the chat.

        Returns:
            SAddUserResponse: The response indicating the result of the 
                operation.
        """
        response: SAddUserResponse
        logger.info(f"adding {user=} to queue in {chat_id=}")
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                logger.debug(f"{queue.id=} exists")
                queue_data = await self.uow.queues.get_with_positions(queue.id)
                if isinstance(queue_data, QueueORM):
                    if await self.uow.users.check_existence(user.id):
                        logger.debug(f"{user.tgid=} exists")
                        position: int = await self.uow.queues.add_position(
                            queue_data, user.id
                        )
                        if position == -1:
                            response = SAddUserResponse(
                                queue_id=queue_data.id, user=user, position=-1)
                        else:
                            response = SAddUserResponse(
                                queue_id=queue.id, user=user, position=position)
                    else:
                        response = SAddUserResponse(
                            queue_id=queue_data.id, user=None, position=-1)
            else:
                response = SAddUserResponse(
                    queue_id=None, user=user, position=-1)
            await self.uow.commit(True)
        logger.info(f"by args {user=}, {chat_id=} got {response=}")
        return response

    async def remove_user(
            self, user: SUser, chat_id: int
    ) -> SRemoveUserResponse:
        """
        Removes a user from the queue.

        Args:
            user (SUser): The user to remove.
            chat_id (int): The ID of the chat.

        Returns:
            SRemoveUserResponse: The response indicating the result of the 
                operation.
        """
        response: SRemoveUserResponse
        logger.info(f"removing {user.id=} from queue in {chat_id=}")
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                queue_data = await self.uow.queues.get_with_positions(queue.id)
                if isinstance(queue_data, QueueORM):
                    if await self.uow.users.check_existence(user.id):
                        result = await self.uow.queues.remove_position(
                            queue, user.id
                        )
                        if not result[0]:
                            logger.debug(
                                f"{user.id=} already not in {queue.id=}")
                            response = SRemoveUserResponse(
                                queue_id=queue.id, user=user, is_already=True)
                        else:
                            logger.debug(f"{user.id=} removed from {queue.id}")
                            response = SRemoveUserResponse(
                                queue_id=queue.id,
                                user=user,
                                notificate_target=result[1]
                            )
                    else:
                        logger.error(f"{user.id=} not found in database")
                        response = SRemoveUserResponse(
                            queue_id=queue.id, user=None)
            else:
                logger.warning(
                    f"atempt quit non-existance queue in {chat_id=}")
                response = SRemoveUserResponse(queue_id=None, user=user)
            await self.uow.commit(True)
        logger.info(f"got {response=} for args=( {user=}, {chat_id=} )")
        return response

    async def clear_queue(self, chat_id: int) -> UUID | None:
        """
        Clears the queue for a given chat.

        Args:
            chat_id (int): The ID of the chat.

        Returns:
            Optional[UUID]: The ID of the cleared queue, or None if the queue 
                does not exist.
        """
        logger.info(f"clearing queue in {chat_id=}")
        async with self.uow:
            queue = await self.uow.queues.get_by_chat_id(chat_id)
            if isinstance(queue, QueueORM):
                logger.debug(f"{queue.id=} exists in {chat_id=}")
                await self.uow.queues.clear(queue.id)
                answer: UUID = queue.id
            else:
                logger.warning(
                    f"atempt clear non-existance queue in {chat_id=}")
                answer = None
            await self.uow.commit(True)
        return answer
