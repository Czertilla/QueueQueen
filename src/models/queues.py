from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from models.positions import PositionORM


class QueueORM(Base):
    """
    SQLAlchemy model representing a queue

    Attributes:
        chat_id (int | None): The chat ID associated with the queue, can be None.
        positions (list[PositionORM]): A list of positions in the queue.
    """

    __tablename__ = "queues"

    chat_id: Mapped[int] = mapped_column(nullable=True)
    positions: Mapped[list[PositionORM]] = relationship(back_populates="queue")
