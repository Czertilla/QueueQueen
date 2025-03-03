from logging import getLogger
from aiogram import Bot, Router
from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner
from aiogram.filters import CommandStart, Command
from bot.messages.messages import MessageTextBuilder
from services.queues import QueueService
from services.users import UserService
from units_of_work.all import AllUOW
from ..messages.localization import i18n_manager

router = Router()

logger = getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    """
    Handles the /start command.

    Updates user information, checks if the user is an admin, and sends a response
    based on the user's permissions.

    Args:
        message (Message): The incoming Message object.
    """
    user = message.from_user
    logger.info(f"handling /start cmd from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    logger.debug(f"getting chat memger info by {user.id=}")
    member = await message.chat.get_member(user.id)
    message_builder = MessageTextBuilder()
    if isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        logger.debug(f"member {user.id=} got enough rights to start bot")
        queue_list = await QueueService(uow).get_queue_list(
            message.chat.id, True)
        await message.answer(await message_builder.on_queue_list(queue_list))
    else:
        logger.debug(f"member got not enouth rights to start bot")
        await message.answer(
            await message_builder.on_not_admin(user_schema.username)
        )


@router.message(Command("join"))
async def join(message: Message) -> None:
    """
    Handles the /join command.

    Adds the user to the queue and sends a response with the result.

    Args:
        message (Message): The incoming Message object.
    """
    user = message.from_user
    logger.info(f"handling /join cmd from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    response = await QueueService(uow).add_user(
        user_schema, message.chat.id
    )
    await message.answer(
        await MessageTextBuilder().on_user_queue_crud(response)
    )


@router.message(Command("quit"))
async def quit(message: Message, bot: Bot) -> None:
    """
    Handles the /quit command.

    Removes the user from the queue, notifies the next user in line, and sends a response.

    Args:
        message (Message): The incoming Message object.
        bot (Bot): The Bot instance.
    """
    user = message.from_user
    logger.info(f"handling /quit cmd from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    message_builder = MessageTextBuilder()
    response = await QueueService(uow).remove_user(user_schema, message.chat.id)
    if response.notificate_target is not None:
        await bot.send_message(
            chat_id=response.notificate_target,
            text=await message_builder.on_your_turn_ntf()
        )
    await message.answer(await message_builder.on_remove_user(response))


@router.message(Command("check"))
async def check(message: Message) -> None:
    """
    Handles the /check command.

    Retrieves and sends the current queue list.

    Args:
        message (Message): The incoming Message object.
    """
    response = await QueueService(AllUOW()).get_queue_list(message.chat.id)
    await message.answer(await MessageTextBuilder().on_queue_list(response))


@router.message(Command("clear"))
async def clear(message: Message) -> None:
    """
    Handles the /clear command.

    Checks if the user is an admin and clears the queue if they are.

    Args:
        message (Message): The incoming Message object.
    """
    user = message.from_user
    await UserService(uow := AllUOW()).update_user(user)
    member = await message.chat.get_member(user.id)
    message_builder = MessageTextBuilder()
    if isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        response = await QueueService(uow).clear_queue(message.chat.id)
        await message.answer(message_builder.on_clear_queue(response))
    else:
        await message.answer(
            await message_builder.on_not_admin(message.from_user.username)
        )