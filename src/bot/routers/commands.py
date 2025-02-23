from aiogram import Bot, Router
from aiogram.types import Message, ChatMemberAdministrator, ChatMemberOwner
from aiogram.filters import CommandStart, Command
from services.queues import QueueService
from services.users import UserService
from units_of_work.all import AllUOW

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    member = await message.chat.get_member(user.id)
    if isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        await message.answer(await QueueService(uow).get_queue_list(message.chat.id, True))
    else:
        await message.answer(f"@{message.from_user.username}, you are not admin. Add this bot to chat, where you`re admin")


@router.message(Command("join"))
async def join(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    await message.answer(await QueueService(uow).add_user(user, message.chat.id))


@router.message(Command("quit"))
async def quit(message: Message, bot: Bot) -> None:
    user = message.from_user
    result = await QueueService(AllUOW()).remove_user(user, message.chat.id)
    if result[1] is not None:
        await bot.send_message(
            chat_id=result[1],
            # text=f"it`s your turn now. Don`t forget quit queue or just push this button",
            text=f"it`s your turn now Don`t forget quit queue"
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
    if isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        await message.answer(await QueueService(uow).clear_queue(message.chat.id))
    else:
        await message.answer(f"@{message.from_user.username}, you are not admin. Add this bot to chat, where you`re admin")
