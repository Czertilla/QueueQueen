from uuid import UUID
from pydantic import BaseModel
from schemas.users import SUser


class SQueueList(BaseModel):
    id: UUID | None
    queue: list[SUser] | None
    is_new: bool = False

    class Config:
        from_atributes = True
