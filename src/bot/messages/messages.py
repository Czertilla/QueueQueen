import logging
from uuid import UUID
from schemas.queues import (
    SAddUserResponse,
    SQueueList,
    SRemoveUserResponse,
    SUserQueueCrudResponse,
)
from utils.settings import getSettings
from .localization import i18n_manager


DEFAULT_MARKUP: str = getSettings().BOT_PARSE_MODE

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MessageTextBuilder:
    """
    Objects of this class construct text for messages in accordance with the
    selected localization and markup languages.
    """

    def __init__(
        self, lang: str | None = None, markup: str = DEFAULT_MARKUP
    ) -> None:
        """
        Initializes the MessageTextBuilder object.

        :param lang: The language for the message (default is None, 
            falls back to default language)
        :param markup: The markup format for the message (default is set 
            from settings)
        """
        self.lang: str | None = lang
        self.markup: str = markup
        logger.debug(
            f"initialized MessageTextBuilder(lang={lang}, markup={markup})")

    async def get_phrase(self, key: str, **kwargs) -> str:
        """
        Asynchronously retrieves a localized phrase.

        :param key: The key for the localized phrase.
        :param kwargs: Additional parameters for string formatting.
        :return: The formatted localized string.
        """
        phrase = await i18n_manager.get(
            key,
            self.lang,
            self.markup,
            **kwargs
        )
        logger.debug(
            f"fetched phrase for key='{key}' with kwargs={kwargs}: '{phrase}'")
        return phrase

    async def on_not_admin(self, username: str) -> str:
        """
        Asynchronously retrieves a message for a user who is not an 
        admin andis trying to do something that only an admin can do.

        :param username: The username to include in the message.
        :return: The localized string with the message.
        """
        logger.debug(f"retrieving message for user @{username}, who not admin")
        return await self.get_phrase(
            "not_admin_alert",
            username=username
        )

    async def on_your_turn_ntf(self) -> str:
        """
        Asynchronously retrieves the notification message for when it's 
        the user's turn.

        :return: The localized string with the message.
        """
        logger.debug("Retrieving turn notification message")
        return await self.get_phrase("head_ntf")

    async def on_queue_list(self, queue_list: SQueueList) -> str:
        """
        Constructs the queue list message.

        :param queue_id: The identifier of the queue.
        :param queue_list: The queue list data.
        :return: The localized queue list message.
        """
        queue_id = queue_list.id
        logger.debug(f"constructing queue list for queue_id={queue_id}.")
        if queue_list.id is None:
            msg_key = "new_queue_err" if queue_list.is_new else "no_queue"
            logger.info(f"no queue during constructing list, ({msg_key=})")
            return await self.get_phrase(msg_key)
        else:
            msg_key = "new_queue" if queue_list.is_new else "queue_list_header"
            logger.debug(f"constructing queue list, {msg_key=}")
            answer = await self.get_phrase(msg_key, queue_id=queue_id)
            if queue_list.positions:
                for p, pos in enumerate(queue_list.positions):
                    answer += f"\n {
                        p} - {pos.first_name} {pos.last_name} (@{pos.username})"
                logger.debug(
                    f"constructed queue list for {len(queue_list.positions)}" +
                    " positions"
                )
            else:
                logger.debug(
                    f"queue turned out empty during constructing list")
                answer += "\n" + await self.get_phrase("empty")

            return answer

    async def on_add_user(self, response: SAddUserResponse) -> str:
        """
        Constructs the message for adding a user to the queue.

        :param response: The response containing user addition details.
        :return: The localized message for user addition.
        """
        queue_id = response.queue_id
        tgid = response.user.tgid
        logger.debug(f"constructing msg for user {tgid=} added to {queue_id=}")
        if response.position == -1:
            logger.debug(f"user {tgid=} turned out already in {queue_id=}")
            return await self.get_phrase(
                "already_in_queue",
                username=response.user.username
            )
        else:
            logger.debug(f"user {tgid=} turned out added to {queue_id=}")
            return await self.get_phrase(
                "new_position_ntf",
                username=response.user.username,
                pos_num=response.position
            )

    async def on_remove_user(self, response: SRemoveUserResponse) -> str:
        """
        Constructs the message for removing a user from the queue.

        :param response: The response containing user removal details.
        :return: The localized message for user removal.
        """
        queue_id = response.queue_id
        tgid = response.user.tgid
        msg_key = "user_not_in_queue" if response.is_already else "user_removed"
        logger.debug(
            f"constructing msg for user {tgid=} rm from {queue_id=}, {msg_key=}"
        )
        return await self.get_phrase(
            msg_key,
            username=response.user.username,
            queue_id=queue_id
        )

    async def on_user_queue_crud(self, response: SUserQueueCrudResponse) -> str:
        """
        Constructs a message based on the type of user in queue CRUD operation 
        performed.

        :param response: The response containing queue operation details.
        :return: The localized message for the operation.
        """
        if response.queue_id is None:
            logger.info(f"constructed queue not found alert")
            return await self.get_phrase("queue_404")
        if response.user is None:
            logger.info(f"constructed user not found alert")
            return await self.get_phrase("user_404")
        if isinstance(response, SAddUserResponse):
            return await self.on_add_user(response)
        if isinstance(response, SRemoveUserResponse):
            return await self.on_remove_user(response)
        message = f"unexpected type of QueueService response given"
        logger.warning(f"{message}, {response=}")
        return f"MessageTextBuilder error: {message}"

    async def on_clear_queue(self, queue_id: int | UUID | str | None) -> str:
        """
        Constructs the message for clearing a queue.

        :param queue_id: The identifier of the queue.
        :return: The localized message for queue clearing.
        """
        if queue_id is None:
            logger.debug(
                f"constructed msg for an attempt to clear a non-existent queue")
            return await self.get_phrase("no_queue")
        else:
            logger.debug(f"constructed msg for clear a queue")
            return await self.get_phrase("queue_cleared", queue_id=queue_id)
