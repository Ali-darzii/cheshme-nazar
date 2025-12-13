from pydantic import BaseModel, EmailStr

class GetEmail(BaseModel):
    email: EmailStr
    
class EmailApproveOtp(GetEmail):
    otp: int
    
class EmailLogin(GetEmail):
    password: str

class CreateRevokeToken(BaseModel):
    jti: str
    user_id: int
    
    
class TokenOut(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str