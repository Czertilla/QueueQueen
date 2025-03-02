from uuid import UUID
from pydantic import BaseModel
from schemas.users import SUser


class SQueueList(BaseModel):
    id: UUID | None
    positions: list[SUser] | None
    is_new: bool = False

    class Config:
        from_attributes = True


class SUserQueueCrudResponse(BaseModel):
    queue_id: UUID | None
    user: SUser | None

    class Config:
        from_attributes = True

class SAddUserResponse(SUserQueueCrudResponse):
    position: int


class SRemoveUserResponse(SUserQueueCrudResponse):
    is_already: bool
