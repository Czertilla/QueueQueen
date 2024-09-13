
from pydantic import BaseModel

class SUser(BaseModel):
    username: str
    tgid: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    

    class Config:
        from_atributes = True
