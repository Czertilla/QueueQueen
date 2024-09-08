from utils.settings import Settings
from utils.mixins.singleton import SingletonMixin
from .contextmanager import lifespan
from utils.settings import getSettings


class Settings(Settings, SingletonMixin):
    app_name: str = getSettings().APP_NAME
    app_presets: dict = {
        'title': app_name,
        'lifespan': lifespan
    }
 