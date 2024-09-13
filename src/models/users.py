from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.sqlalchemy.base import IdMinxin
from models.positions import PositionORM

if TYPE_CHECKING:
    from models import QueueORM


class UserORM(Base):
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


