from logging import getLogger
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner
from aiogram.exceptions import TelegramForbiddenError

from bot.keyboards.inline import InlineBuilder
from bot.messages.messages import MessageTextBuilder
from services.queues import QueueService
from services.users import UserService
from units_of_work.all import AllUOW
from utils.enums.callbacks import CallbackPrefix
from utils.enums.locales import LocaleKey

router = Router()

logger = getLogger(__name__)


@router.callback_query(F.data.startswith(CallbackPrefix.quit))
async def quit(call: CallbackQuery, bot: Bot):
    user = call.from_user
    logger.info(f"handling {call.data=} from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    message_builder = MessageTextBuilder(lang=user.language_code)
    logger.debug(f"getting chat_id from {call.data=} to quit from queue")
    chat_id_str = call.data[len(CallbackPrefix.quit) :]
    try:
        chat_id = int(chat_id_str)
    except ValueError as e:
        logger.error(
            f"durring handling {call.data=} from {user.id=}, "
            + f"invalid callback got {chat_id_str=}"
        )
        await call.message.reply(
            await message_builder.get_phrase(LocaleKey.invalid_callback)
        )
        return
    response = await QueueService(uow).remove_user(user_schema, chat_id)
    if response.notificate_target is not None:
        await bot.send_message(
            chat_id=response.notificate_target,
            text=await message_builder.on_your_turn_ntf(response.queue_id),
            reply_markup=await InlineBuilder(message_builder).quit_kb(chat_id),
        )
    await call.message.edit_reply_markup()
    await bot.send_message(
        chat_id=chat_id, text=await message_builder.on_remove_user(response)
    )


@router.callback_query(F.data == "queue/join")
async def join(call: CallbackQuery) -> None:
    """
    Handles the /join command.

    Adds the user to the queue and sends a response with the result.

    Args:
        message (Message): The incoming Message object.
    """
    user = call.from_user
    logger.info(f"handling /join cmd from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    await (service := QueueService(uow)).add_user(
        user_schema, call.message.chat.id
    )
    response = await service.get_queue_list(call.message.chat.id)
    await call.message.edit_text(
        await (mb := MessageTextBuilder(lang=user.language_code)).on_queue_list(
            response
        ),
        reply_markup=await InlineBuilder(mb).queue_kb()
    )


@router.callback_query(F.data == "queue/quit")
async def quit_queue(call: CallbackQuery, bot: Bot):
    user = call.from_user
    message = call.message
    logger.info(f"handling /quit cmd from {user.id=}")
    user_schema = await UserService(uow := AllUOW()).update_user(user)
    message_builder = MessageTextBuilder(lang=user.language_code)
    response = await (service := QueueService(uow)).remove_user(
        user_schema, message.chat.id
    )
    if response.notificate_target is not None:
        try:
            await bot.send_message(
                chat_id=response.notificate_target,
                text=await message_builder.on_your_turn_ntf(response.queue_id),
                reply_markup=await InlineBuilder(message_builder).quit_kb(
                    message.chat.id
                ),
            )
        except TelegramForbiddenError as exc:
            logger.warning(
                "attempt to send notification to user.id="
                + f"{response.notificate_target} was denied. Raised {exc=}"
            )
    response = await service.get_queue_list(call.message.chat.id)
    await call.message.edit_text(
        await (mb := MessageTextBuilder(lang=user.language_code)).on_queue_list(
            response
        ),
        reply_markup=await InlineBuilder(mb).queue_kb()
    )


@router.callback_query(F.data.startswith(CallbackPrefix.kick))
async def kick(call: CallbackQuery, bot: Bot):
    user = call.from_user
    member = await bot.get_chat_member(call.message.chat.id, user.id)
    logger.info(f"handling {call.data=} from {user.id=}")
    message_builder = MessageTextBuilder(lang=user.language_code)
    if not isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        logger.debug("member got not enouth rights to kick user")
        await call.message.answer(
            await message_builder.on_not_admin(user.username)
        )
        return
    target_tgid_str = call.data[len(CallbackPrefix.kick.value) :]
    try:
        target_tgid = int(target_tgid_str)
    except ValueError as e:
        logger.error(
            f"durring handling {call.data=} from {user.id=}, "
            + f"invalid callback got {target_tgid_str=}"
        )
        await call.message.reply(
            await message_builder.get_phrase(LocaleKey.invalid_callback)
        )
        return
    target_member = await bot.get_chat_member(call.message.chat.id, target_tgid)
    target_user = getattr(target_member, "user", None)
    if target_user is None:
        logger.error(f"got unexists user during handling {call.data=}")
        await call.message.reply(
            await message_builder.get_phrase(LocaleKey.invalid_callback)
        )
        return
    user_schema = await UserService(uow := AllUOW()).update_user(target_user)
    response = await QueueService(uow).remove_user(
        user_schema, call.message.chat.id
    )
    if response.notificate_target is not None:
        await bot.send_message(
            chat_id=response.notificate_target,
            text=await message_builder.on_your_turn_ntf(response.queue_id),
            reply_markup=await InlineBuilder(message_builder).quit_kb(
                call.message.chat.id
            ),
        )
    await call.message.answer(await message_builder.on_remove_user(response))
    await call.message.delete()


@router.callback_query(F.data.startswith(CallbackPrefix.cansel))
async def cansel(call: CallbackQuery, bot: Bot):
    user = call.from_user
    member = await bot.get_chat_member(call.message.chat.id, user.id)
    logger.info(f"handling {call.data=} from {user.id=}")
    message_builder = MessageTextBuilder(lang=user.language_code)
    if not isinstance(member, ChatMemberAdministrator | ChatMemberOwner):
        logger.debug(f"member got not enouth rights to kick user")
        await call.message.answer(
            await message_builder.on_not_admin(user.username)
        )
        return
    await call.message.delete()
