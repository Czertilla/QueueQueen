
from uuid import UUID
from pydantic import BaseModel

class SUser(BaseModel):
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
