from enum import Enum
import logging
from uuid import UUID
from schemas.queues import (
    SAddUserResponse,
    SQueueList,
    SRemoveUserResponse,
    SUserQueueCrudResponse,
)
from utils.enums.locales import LocaleKey
from utils.settings import getSettings
from .localization import i18n_manager

DEFAULT_MARKUP: str = getSettings().BOT_PARSE_MODE.value

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MessageTextBuilder:
    """A class responsible for constructing localized message texts with
    appropriate markup formatting.
    """

    def __init__(
            self, lang: str | None = None, markup: str = DEFAULT_MARKUP
    ) -> None:
        """
        Initializes a MessageTextBuilder instance.

        Args:
            lang (str | None, optional): The language for the message.
                Defaults to None (falls back to default).
            markup (str, optional): The markup format for messages.
                Defaults to `DEFAULT_MARKUP`.
        """
        self.lang: str | None = lang
        self.markup: str = markup
        logger.debug(
            f"initialized MessageTextBuilder(lang={lang}, markup={markup})")

    async def get_phrase(self, key: str | Enum, **kwargs) -> str:
        """
        Retrieves a localized phrase asynchronously.

        Args:
            key (str): The key identifier for the phrase.
            **kwargs: Additional parameters for formatting.

        Returns:
            str: The localized and formatted phrase.
        """
        if isinstance(key, Enum):
            key = str(key.value)
        phrase = await i18n_manager.get(key, self.lang, self.markup, **kwargs)
        logger.debug(
            f"fetched phrase for key='{key}' with kwargs={kwargs}: '{phrase}'")
        return phrase

    async def on_not_admin(self, username: str) -> str:
        """
        Returns a message notifying that the user is not an admin.

        Args:
            username (str): The username of the non-admin user.

        Returns:
            str: The localized message.
        """
        logger.debug(f"retrieving message for non-admin user @{username}")
        return await self.get_phrase(
            LocaleKey.not_admin_alert, username=username
        )

    async def on_your_turn_ntf(self, queue_id: UUID) -> str:
        """
        Returns a notification message when it's the user's turn.

        Args:
            queue_id (UUID): Еру id of the queue that the notified user is head

        Returns:
            str: The localized message.
        """
        logger.debug("Retrieving turn notification message")
        return await self.get_phrase(LocaleKey.head_ntf, queue_id=queue_id.hex)

    async def on_queue_list(self, queue_list: SQueueList) -> str:
        """
        Constructs a message listing the queue's participants.

        Args:
            queue_list (SQueueList): The queue list data.

        Returns:
            str: The formatted queue list message.
        """
        queue_id = queue_list.id
        logger.debug(f"Constructing queue list for queue_id={queue_id}")

        if queue_list.id is None:
            msg_key = "new_queue_err" if queue_list.is_new else "no_queue"
            logger.info(f"no queue found, using message key: {msg_key}")
            return await self.get_phrase(msg_key)

        msg_key = "new_queue" if queue_list.is_new else "queue_list_header"
        logger.debug(f"constructing queue list, {msg_key=}")
        answer = await self.get_phrase(msg_key, queue_id=queue_id.hex)

        if queue_list.positions:
            for p, pos in enumerate(queue_list.positions):
                answer += f"\n {p} - {pos.first_name} {pos.last_name} (@{pos.username})"
            logger.debug(
                f"constructed queue list with {len(queue_list.positions)}"
                + " positions"
            )
        else:
            logger.debug("queue is empty")
            answer += "\n" + await self.get_phrase(LocaleKey.empty)

        return answer

    async def on_add_user(self, response: SAddUserResponse) -> str:
        """
        Constructs a message for adding a user to the queue.

        Args:
            response (SAddUserResponse): The response containing user addition
                details.

        Returns:
            str: The localized message.
        """
        queue_id = response.queue_id
        tgid = response.user.tgid
        logger.debug(f"constructing msg for user {tgid=} added to {queue_id=}")

        if response.position == -1:
            logger.debug(f"user {tgid} is already in queue {queue_id}")
            return await self.get_phrase(
                LocaleKey.already_in_queue, username=response.user.username
            )
        else:
            logger.debug(f"user {tgid=} turned out added to {queue_id=}")
            return await self.get_phrase(
                LocaleKey.new_position_ntf,
                username=response.user.username,
                pos_num=response.position,
            )

    async def on_remove_user(self, response: SRemoveUserResponse) -> str:
        """
        Constructs a message for removing a user from the queue.

        Args:
            response (SRemoveUserResponse): The response containing user removal
                details.

        Returns:
            str: The localized message.
        """
        queue_id = response.queue_id
        tgid = response.user.tgid
        msg_key = "user_not_in_queue" if response.is_already else "user_removed"
        logger.debug(
            f"constructing msg for user {tgid=} rm from {queue_id=}, {msg_key=}"
        )
        return await self.get_phrase(
            msg_key, username=response.user.username, queue_id=queue_id.hex
        )

    async def on_user_queue_crud(self, response: SUserQueueCrudResponse) -> str:
        """
        Constructs a message based on a CRUD operation performed on the queue.

        Args:
            response (SUserQueueCrudResponse): The response containing queue
                operation details.

        Returns:
            str: The localized message.
        """
        if response.queue_id is None:
            logger.info("constructed queue not found alert")
            return await self.get_phrase(LocaleKey.queue_404)
        if response.user is None:
            logger.info("constructed user not found alert")
            return await self.get_phrase(LocaleKey.user_404)
        if isinstance(response, SAddUserResponse):
            return await self.on_add_user(response)
        if isinstance(response, SRemoveUserResponse):
            return await self.on_remove_user(response)
        message = f"unexpected type of QueueService response given"
        logger.warning(f"{message}, {response=}")
        return f"MessageTextBuilder error: {message}"

    async def on_clear_queue(self, queue_id: int | UUID | str | None) -> str:
        """
        Constructs a message indicating a queue has been cleared.

        Args:
            queue_id (int | UUID | str | None): The queue identifier.

        Returns:
            str: The localized message.
        """
        if queue_id is None:
            logger.debug("attempted to clear a non-existent queue")
            return await self.get_phrase(LocaleKey.no_queue)

        logger.debug("constructed msg for clear a queue")
        return await self.get_phrase(LocaleKey.queue_cleared, queue_id=queue_id.hex)
