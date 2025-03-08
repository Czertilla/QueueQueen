from utils.settings import Settings
from utils.mixins.singleton import SingletonMixin
from .contextmanager import lifespan
from utils.settings import getSettings


class Settings(Settings, SingletonMixin):
    """
    Application settings class, inheriting from `Settings` and `SingletonMixin`.

    This class provides application-specific settings, including the application
     name and presets for the FastAPI application. It ensures that only one
     instance of the settings object is created due to the `SingletonMixin`.

    Attributes:
        app_name (str): The name of the application, retrieved from global 
            settings.
        app_presets (dict): A dictionary containing presets for the FastAPI 
            application, including the title and lifespan context manager.
    """

    app_name: str = getSettings().APP_NAME
    app_presets: dict = {"title": app_name, "lifespan": lifespan}
