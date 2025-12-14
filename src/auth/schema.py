from enum import Enum
from pydantic import BaseModel, EmailStr

from src.auth.helper.jwt import TokenType

class GetEmail(BaseModel):
    email: EmailStr
    
class EmailApproveOtp(GetEmail):
    otp: int
    
class EmailLogin(GetEmail):
    password: str

class CreateRevokeToken(BaseModel):
    jti: str
    user_id: int
    
class TokenType(str, Enum):
    access_token = "access"
    refresh_token = "refresh"


class TokenOut(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    
class TokenVerifyOut(BaseModel):
    access_token: str
    token_type: TokenType