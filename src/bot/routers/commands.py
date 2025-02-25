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
    user = message.from_user
    logger.info(f"handling /start cmd from {user.id=}")
    await UserService(uow := AllUOW()).check_user(user)
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
            await message_builder.on_not_admin(message.from_user.username)
        )


@router.message(Command("join"))
async def join(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    await message.answer(await QueueService(uow).add_user(user, message.chat.id))


@router.message(Command("quit"))
async def quit(message: Message, bot: Bot) -> None:
    user = message.from_user
    message_builder = MessageTextBuilder()
    result = await QueueService(AllUOW()).remove_user(user, message.chat.id)
    if result[1] is not None:
        await bot.send_message(
            chat_id=result[1],
            # text=f"it`s your turn now. Don`t forget quit queue or just push this button",
            text=await message_builder.on_your_turn_ntf()
        )
    await message.answer(result[0])


@router.message(Command("check"))
async def check(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    await message.answer(await QueueService(uow).get_queue_list(message.chat.id))


@router.message(Command("clear"))
async def clear(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    member = await message.chat.get_member(user.id)
    message_builder = MessageTextBuilder()
    if isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        await message.answer(await QueueService(uow).clear_queue(message.chat.id))
    else:
        await message.answer(
            await message_builder.on_not_admin(message.from_user.username)
        )
