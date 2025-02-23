import asyncio
import sys
import os
from logging import Formatter, StreamHandler, getLogger, DEBUG

logger = getLogger()
logger.setLevel(DEBUG)
if not logger.hasHandlers():
    handler = StreamHandler()  # Вывод в консоль (stdout)
    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

parent_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
    )
sys.path.append(parent_directory)

from src.bot import bot, dp


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))