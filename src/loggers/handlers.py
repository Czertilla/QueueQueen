import gzip
import os
import shutil
import glob
from logging.handlers import TimedRotatingFileHandler
import asyncio
import traceback
from aiogram import Bot
from aiogram.types import InputMediaDocument, BufferedInputFile
from logging import CRITICAL, LogRecord, Handler, getLogger

from utils.settings import getSettings


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Timed rotating file handler with automatic gzip compression."""

    def doRollover(self):
        """Compresses the rotated log file using gzip."""
        super().doRollover()

        for old_log in glob.glob(self.baseFilename + ".*"):
            if not old_log.endswith(".gz"):
                with open(old_log, "rb") as f_in:
                    with gzip.open(f"{old_log}.gz", "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(old_log)


class TelegramLogHandler(Handler):
    """Custom log handler to send critical logs to Telegram."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = getSettings()
        self.bot = Bot(token=settings.BOT_TG_TOKEN)
        self.chat_id_list = settings.DEV_ID_LIST

    def emit(self, record: LogRecord):
        """Sends a log record to Telegram asynchronously."""
        try:
            log_entry = self.format(record)
            event_loop = asyncio.get_event_loop()
            task = self._send_to_telegram(log_entry, record.exc_info)
            if event_loop.is_running():
                event_loop.create_task(task)
            else:
                asyncio.run(task)
        except Exception:
            # Логируем ошибку, если что-то пошло не так
            self.handleError(record)

    async def _send_to_telegram(self, message: str, exc_info):
        """Asynchronously sends a message to Telegram."""
        message_text = f"🔥 CRITICAL LOG:\n{message}"
        if exc_info is not None:
            trace = "".join(traceback.format_exception(*exc_info))
            document = InputMediaDocument(media=BufferedInputFile(
                file=trace.encode(), filename="traceback.txt"
            ), caption=message_text)
        else:
            document = None
        for chat_id in self.chat_id_list:
            try:
                tg_message = await self.bot.send_message(
                    chat_id=chat_id,
                    text= message_text,
                    parse_mode="HTML"
                )
                if document:
                    await tg_message.edit_media(media=document)
            except Exception as e:
                getLogger("TG_LOG_HANDLER").error(
                    f"Send tg msg error", exc_info=e)
