import re
from datetime import datetime

from pydantic import BaseModel, field_validator, Field, EmailStr

from src.user.model import UserRole
from src.utils.general_exception import GeneralErrorReponses

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    
    @field_validator("password", mode="after")
    def validate_password(cls, v: str) -> str:
        """
        - 8 to 40 characters.
        - At least contain 1 number.
        - At least contain 1 letter.
        - At least contain 1 captal letter.

        """
        regex = re.compile(r"^(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*\d).{8,50}$")
        if not regex.match(v):
            raise GeneralErrorReponses.bad_format("password")
        
        return v
    
class UserOut(BaseModel):
    id: int
    email: str
    role: UserRole
    email_approved: bool
    created_at: datetime
    updated_at: datetime | None
    
class UpdateUser(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None    