from pydantic import BaseModel, EmailStr

from src.user.schema import UserOut


class TokenOut(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str

class EmailSendOtp(BaseModel):
    email: EmailStr
    
class EmailApproveOtp(EmailSendOtp):
    otp: int