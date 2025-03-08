from typing import TYPE_CHECKING
from uuid import UUID
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.mixins.sqlalchemy import TimestampMixin

if TYPE_CHECKING:
    from models import UserORM
    from models import QueueORM


class PositionORM(Base, TimestampMixin):
    """
    SQLAlchemy model representing a position in a queue.

    Attributes:
        user_id (UUID): The UUID of the user, foreign key referencing users.id.
        queue_id (UUID): The UUID of the queue, foreign key referencing queues.id.
        user (UserORM): The user associated with the position.
        queue (QueueORM): The queue associated with the position.
        position (int | None): The position number in the queue, can be None.
    """

    __tablename__ = "positions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    queue_id: Mapped[UUID] = mapped_column(
        ForeignKey("queues.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["UserORM"] = relationship(
        foreign_keys=[user_id], back_populates="positions"
    )
    queue: Mapped["QueueORM"] = relationship(
        foreign_keys=[queue_id], back_populates="positions"
    )

    position: Mapped[int | None] = mapped_column(nullable=True)
