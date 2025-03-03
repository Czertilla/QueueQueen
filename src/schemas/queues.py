from uuid import UUID
from pydantic import BaseModel
from schemas.users import SUser
from typing import Optional


class SQueueList(BaseModel):
    """
    Schema for representing a queue list.

    Attributes:
        id (UUID | None): The unique identifier of the queue,
            or None if not available.
        positions (list[SUser] | None): A list of users in the queue,
            or None if not available.
        is_new (bool): Indicates if the queue is newly created.
    """
    id: UUID | None
    positions: list[SUser] | None
    is_new: bool = False

    class Config:
        from_attributes = True


class SUserQueueCrudResponse(BaseModel):
    """
    Schema for representing a user queue CRUD response.

    Attributes:
        queue_id (UUID | None): The unique identifier of the queue,
            or None if not available.
        user (SUser | None): The user involved in the operation,
            or None if not available.
    """
    queue_id: UUID | None
    user: SUser | None

    class Config:
        from_attributes = True


class SAddUserResponse(SUserQueueCrudResponse):
    """
    Schema for representing a response to adding a user
    to a queue.

    Attributes:
        queue_id (UUID | None): The unique identifier of the queue,
            or None if not available.
        user (SUser | None): The user involved in the operation,
            or None if not available.
        position (int): The position of the user in the queue.
    """
    position: int


class SRemoveUserResponse(SUserQueueCrudResponse):
    """
    Schema for representing a response to removing a user
    from a queue.

    Attributes:
        queue_id (UUID | None): The unique identifier of the queue,
            or None if not available.
        user (SUser | None): The user involved in the operation,
            or None if not available.
        is_already (bool): Indicates if the user was already
            not in the queue.
        notificate_target (int | None): Telegram ID of the user
            to notify, or None if no notification is needed.
    """
    is_already: bool = False
    notificate_target: int | None = None