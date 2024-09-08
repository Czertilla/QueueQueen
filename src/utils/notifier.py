from functools import lru_cache
from notifiers.logging import NotificationHandler
import notifiers
from src.utils.settings import getSettings

settings = getSettings()
params = {
    "token": settings.NOTIFIER_TG_TOKEN,
    "chat_id": settings.NOTIFIER_TG_CHAT
}

# Send a single notification
notifier = notifiers.get_notifier("telegram")

# Be alerted on each error message


@lru_cache()
def get_handler():
    notifier.notify(
        message=f"this chat has been got for logs notifications by {
            settings.APP_NAME}",
        **params)
    return NotificationHandler("telegram", defaults=params)
