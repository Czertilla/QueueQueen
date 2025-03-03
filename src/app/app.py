from fastapi import FastAPI
from .config import Settings
from api.routers import include_routers

"""
This module initializes and configures the FastAPI application.

It creates an instance of FastAPI, applies settings from the 
`app.Settings` class, and includes routers from the `api.routers` module.

The resulting `app` object is the main FastAPI application instance.
"""

app = FastAPI(**Settings().app_presets)
include_routers(app)
