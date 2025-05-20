
from pydantic import BaseModel

from app.schemas.users import UserOut


class Responseloggin(BaseModel):
    user: UserOut
    access_token: str