from uuid import UUID
from pydantic import BaseModel

class SUser(BaseModel):
    """
    Schema for representing user information.

    Attributes:
        id (UUID): The unique identifier of the user.
        username (str): The username of the user.
        tgid (int): The Telegram ID of the user.
        is_bot (bool): Indicates if the user is a bot.
        first_name (str): The first name of the user.
        last_name (str | None): The last name of the user, if available.
        username (str | None): The username of the user, if available.
        language_code (str | None): The language code of the user, if available.
    """
    id: UUID
    username: str
    tgid: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None

    class Config:
        from_attributes = True