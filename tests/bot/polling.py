import asyncio
import sys
import sys
import os

parent_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
    )
sys.path.append(parent_directory)

from src.bot import bot, dp



if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))