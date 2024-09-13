from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.sqlalchemy.base import IdMinxin
from models.positions import PositionORM

if TYPE_CHECKING:
    from models import UserORM


class QueueORM(Base):
    __tablename__ = "queues"

    chat_id: Mapped[int] = mapped_column(nullable=True)
    positions: Mapped[list[PositionORM]] = relationship(
        back_populates="queue"
    )

