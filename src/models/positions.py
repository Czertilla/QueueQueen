from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from models import UserORM
    from models import QueueORM 


class PositionORM(Base):
    __tablename__ = "positions"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    queue_id: Mapped[UUID] = mapped_column(ForeignKey("queues.id", ondelete="CASCADE"), primary_key=True)

    user: Mapped["UserORM"] = relationship(back_populates="positions")
    queue: Mapped["QueueORM"] = relationship(back_populates="positions")

    position: Mapped[int] = mapped_column(nullable=True)
