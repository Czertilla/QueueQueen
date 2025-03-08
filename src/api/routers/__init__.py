from fastapi import FastAPI, APIRouter
from utils.imports import load_common


routers = load_common(__name__, "router", APIRouter)


def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
