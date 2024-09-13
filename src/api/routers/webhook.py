from aiogram.types import Message, Update, ChatMemberAdministrator, ChatMemberOwner
from aiogram.filters import CommandStart, Command
from fastapi import APIRouter
from fastapi.requests import Request

from services.queues import QueueService
from services.users import UserService
from utils.settings import Settings
from api.dependencies import AllUOW
from bot import bot
settings = Settings()

dp = bot.dp

router = APIRouter(prefix="/webhook", tags=["webhook"])

@dp.message(CommandStart())
async def start(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    member = await message.chat.get_member(user.id)
    if isinstance(member, ChatMemberAdministrator| ChatMemberOwner):
        await message.answer(await QueueService(uow).check_chat(message.chat.id, True))  
    else:
        await message.answer(f"@{message.from_user.username}, you are not admin. Add this bot to chat, where you`re admin")


@dp.message(Command("join"))
async def join(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    await message.answer(await QueueService(uow).add_user(user, message.chat.id))


@dp.message(Command("quit"))
async def quit(message: Message) -> None:
    user = message.from_user
    result = await QueueService(AllUOW()).remove_user(user, message.chat.id)
    if result[1] is not None:
        await bot.send_message(
            chat_id=result[1], 
            # text=f"it`s your turn now. Don`t forget quit queue or just push this button",
            text=f"it`s your turn now Don`t forget quit queue"
        )
    await message.answer(result[0])

@dp.message(Command("check"))
async def check(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    await message.answer(await QueueService(uow).check_chat(message.chat.id))

@dp.message(Command("clear"))
async def check(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    member = await message.chat.get_member(user.id)
    if isinstance(member, ChatMemberAdministrator| ChatMemberOwner):
        await message.answer(await QueueService(uow).clear_queue(message.chat.id))
    else:
        await message.answer(f"@{message.from_user.username}, you are not admin. Add this bot to chat, where you`re admin")

@router.post("")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
