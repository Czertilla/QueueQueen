from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from models.positions import PositionORM


class UserORM(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        username (str | None): The username of the user, can be None.
        tgid (int): The Telegram ID of the user, primary key.
        first_name (str | None): The first name of the user, can be None.
        last_name (str | None): The last name of the user, can be None.
        language_code (str | None): The language code of the user, can be None.
        is_bot (bool): Indicates if the user is a bot.
        positions (list[PositionORM]): A list of positions associated with the user.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=True)
    tgid: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    language_code: Mapped[str] = mapped_column(nullable=True)
    is_bot: Mapped[bool] = mapped_column()

    positions: Mapped[list[PositionORM]] = relationship(
        back_populates="user"
    )
