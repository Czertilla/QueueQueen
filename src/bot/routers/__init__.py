from aiogram import Dispatcher, Router
from importlib import __import__
routers: list[Router] = [

]


def register_routers(dp: Dispatcher) -> None:
    dp.include_routers(*routers)


__all__ = ['register_routers']
