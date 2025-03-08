from aiogram import Dispatcher, Router
from utils.imports import load_common

routers = load_common(__name__, "router", Router)


def register_routers(dp: Dispatcher) -> None:
    dp.include_routers(*routers)


__all__ = ["register_routers"]
