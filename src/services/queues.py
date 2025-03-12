from logging import getLogger
from uuid import UUID
from models.positions import PositionORM
from models.queues import QueueORM
from models.users import UserORM
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
        logger.info(f"constructing queue list for {chat_id=}")
        out_msg = (
            lambda: f"by args {chat_id=}, {from_admin=} got {response=}")
        async with self.uow:
            queue = await self._get_queue_with_positions(chat_id)
            if queue:
                logger.debug(f"{queue.id=} exists")
                positions = self._get_sorted_positions(queue)
                response = SQueueList(id=queue.id, positions=positions)
                logger.info(out_msg())
                return response
            if from_admin:
                logger.debug(
                    f"queue for {chat_id=} not exists, creating by admin")
                queue_id = await self._create_queue(chat_id)
                response = (
                    SQueueList(id=queue_id, positions=[], is_new=True)
                    if queue_id else
                    SQueueList(id=None, positions=None, is_new=True)
                )
                logger.info(out_msg())
                return response
            logger.debug(f"queue for {chat_id=} not exists, no creating")
            response = SQueueList(id=None, positions=None, is_new=False)
            logger.info(out_msg())
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
        logger.info(f"adding {user=} to queue in {chat_id=}")
        out_msg = (
            lambda: f"by args {user=}, {chat_id=} got {response=}"
        )
        async with self.uow:
            queue = await self._get_queue_with_positions(chat_id)
            if queue is None:
                logger.warning(
                    f"attempt join non-existance queue in {chat_id=}")
                response = SAddUserResponse(
                    queue_id=None, user=user, position=-1)
                logger.info(out_msg())
                return response
            logger.debug(f"{queue.id=} exists")
            if not await self.uow.users.check_existence(user.id):
                logger.error(f"{user.tgid=} not exists by id={user.id}")
                response = SAddUserResponse(
                    queue_id=queue.id, user=None, position=-1
                )
                logger.warning(f"unexpected behavor: {out_msg()}")
                return response
            position: int = await self.uow.queues.add_position(
                queue, user.id
            )
            response = SAddUserResponse(
                queue_id=queue.id,
                user=user,
                position=position,
                is_already=position == -1
            )
            await self.uow.commit(True)
            logger.info(out_msg())
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
        logger.info(f"removing {user.id=} from queue in {chat_id=}")
        out_msg = (
            lambda: f"got {response=} for args=( {user=}, {chat_id=} )"
        )
        async with self.uow:
            queue = await self._get_queue_with_positions(chat_id)
            if queue is None:
                logger.warning(
                    f"attempt quit non-existance queue in {chat_id=}")
                response = SRemoveUserResponse(queue_id=None, user=user)
                logger.info(out_msg())
                return response
            if not await self.uow.users.check_existence(user.id):
                logger.error(f"{user.tgid=} not exists by id={user.id}")
                response = SRemoveUserResponse(queue_id=queue.id, user=None)
                logger.warning(f"unexpected behavor: {out_msg()}")
                return response
            result = await self.uow.queues.remove_position(
                queue, user.id
            )
            logger.debug(
                f"{user.id=} removed from {queue.id}"
                if result[0] else f"{user.id=} already not in {queue.id=}")
            response = SRemoveUserResponse(
                queue_id=queue.id,
                user=user,
                is_already=not result[0],
                notificate_target=result[1]
            )
            await self.uow.commit(True)
            logger.info(out_msg())
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
            if not isinstance(queue, QueueORM):
                logger.warning(
                    f"atempt clear non-existance queue in {chat_id=}")
                return None
            logger.debug(f"{queue.id=} exists in {chat_id=}")
            await self.uow.queues.clear(queue.id)
            answer: UUID = queue.id
            await self.uow.commit(True)
        return answer

    async def check_position(
            self, target: str | int, chat_id: int
    ) -> SRemoveUserResponse | None:
        """
        Check position in queue for given chat by target username or position number.

        Args:
            target (str | int): Target user's username or position number.

        Returns:
            SRemoveUserResponse: information about existance queue and user
            or `None` if some porblems during checking
        """
        logger.debug(f"check position {target=} for chat")
        out_msg = (
            lambda: f"{response=} during checking position for {target=},"
            + f" {chat_id=}"
        )
        async with self.uow:
            queue = await self._get_queue_with_positions(chat_id)
            if queue is None:
                logger.warning(
                    "attempt to check position in non-existent queue "
                    + f"{chat_id=}")
                response = SRemoveUserResponse(user=None, queue_id=None)
                logger.info(out_msg())
                return response
            if target.isdigit():
                logger.debug(f"position index was given as {target=}")
                pos_idx = int(target)
                if 0 <= pos_idx < len(queue.positions):
                    response = await self._get_user_from_position(
                        queue, pos_idx
                    )
                    logger.info(out_msg())
                    return response
                logger.debug(
                    f"Position {target} not found in queue {chat_id=}")
                response = SRemoveUserResponse(user=None, queue_id=queue.id)
                logger.info(out_msg())
                return response
            logger.debug(f"username wa given as {target=}")
            response = await self._get_user_from_username(queue, target)
            logger.info(out_msg())
            return response
        
    async def _get_queue_with_positions(self, chat_id: int) -> QueueORM | None:
        """
        Retrieves the queue list for a given chat.

        Do not call this method outside of `uow` Context manager

        Args:
            chat_id (int): Telegram chat id

        Returns:
            QueueORM | None: queue ORM model with positons, or `None`, if it
            not exists
        """
        queue = await self.uow.queues.get_by_chat_id(chat_id)
        if not isinstance(queue, QueueORM):
            return queue
        queue_with_positions = await self.uow.queues.get_with_positions(
            queue.id
        )
        if not isinstance(queue_with_positions, QueueORM):
            logger.critical(
                f"Unexpected behavior: {queue.id} exists, "
                + "but None is returned not QueueORM instance with positions")
            return None
        return queue_with_positions

    async def _create_queue(self, chat_id: int) -> UUID | None:
        """
        Retrieves the queue, just created for a given chat_id

        Args:
            chat_id (int): _description_

        Returns:
            UUID | None: _description_
        """
        queue_id = await self.uow.queues.add_one({"chat_id": chat_id})
        if isinstance(queue_id, UUID):
            logger.info(f"new {queue_id=} created for {chat_id=}")
            await self.uow.commit(True)
        else:
            logger.error(
                f"some problem during attemp to crete queue for {chat_id=}")
        return queue_id

    def _get_sorted_positions(self, queue: QueueORM) -> list[SUser]:
        """
        Retrieves the sorted list of positions from giver QueueORM instance

        Gets positions from ORM model, sort it and convert to list of SUser

        Args:
            queue (QueueORM): ORM model of qeueu, contains target positions

        Returns:
            list[SUser]: list of SUser schemas, contains data about each 
            position in queue
        """
        logger.debug("sorting positions by timestamps")
        positions: list[SUser] = [
            SUser.model_validate(pos.user)
            for pos in sorted(
                queue.positions, key=lambda pos: pos.created_at
            )
        ]
        logger.debug(f"{len(positions)} positions retrieved and sorted")
        return positions


    async def _get_user_from_position(
            self, queue: QueueORM, pos_idx: int
    ) -> SRemoveUserResponse | None:
        """
        Retrieves user information based on position index in the queue.

        Args:
            queue (QueueORM): The queue object containing user positions.
            pos_idx (int): The index of the user position in the queue.

        Returns:
            SRemoveUserResponse | None: A response object containing user details 
            if found, otherwise None.
        """
        position = queue.positions[pos_idx]
        if not isinstance(position, PositionORM):
            logger.critical(
                f"Unexpected position type for {queue.id=}, got "
                + f"{type(position)}")
            return None
        logger.debug(f"Fetching user from position {position.id=}")
        user = await self.uow.users.get(position.user_id)
        if not isinstance(user, UserORM):
            logger.critical(
                f"Unexpected user type for {position.id=}, got {type(user)}")
            return None
        return SRemoveUserResponse(
            queue_id=queue.id, user=SUser.model_validate(user)
        )

    async def _get_user_from_username(
            self, queue: QueueORM, username: str
    ) -> SRemoveUserResponse:
        """
        Retrieves user information based on username from the queue.

        Args:
            queue (QueueORM): The queue object containing user positions.
            username (str): The username of the target user.

        Returns:
            SRemoveUserResponse: A response object containing user details, 
            or indicating if the user is not in the queue.
        """
        user = await self.uow.users.get_by_username(username)
        if not isinstance(user, UserORM):
            logger.debug(f"Unknown username={username}")
            return SRemoveUserResponse(user=None, queue_id=queue.id)
        positions = list(filter(
            lambda pos: isinstance(pos, PositionORM) and pos.user_id == user.id,
            queue.positions
        ))
        if not positions:
            logger.debug(f"{user.id=} not in {queue.id=}")
            return SRemoveUserResponse(
                user=SUser.model_validate(user),
                queue_id=queue.id,
                is_already=True
            )
        if len(positions) > 1:
            logger.critical(
                f"Unexpected positions count for {user.id=} in {queue.id=}")
            return None
        return SRemoveUserResponse(
            user=SUser.model_validate(user), queue_id=queue.id
        )
