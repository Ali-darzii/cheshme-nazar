from pydantic import BaseModel

from src.user.schema import UserOut

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str

class UserTokenOut(UserOut,TokenOut):
    pass