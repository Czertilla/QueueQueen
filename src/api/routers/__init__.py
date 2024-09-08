from fastapi import FastAPI
from .webhook import router as webhook_router
routers = (
    webhook_router,
)


def include_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
