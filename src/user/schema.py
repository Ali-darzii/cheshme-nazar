import re
from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from fastapi import HTTPException, status

from src.auth.schema import TokenOut
from src.utils.general_exception import GeneralErrorReponses

class CreateUser(BaseModel):
    username: str
    password: str
    phone_number: str
    
    @field_validator("username", mode="after")
    def validate_username(cls, v: str) -> str:
        """
        - 5 to 32 characters.
        - Start with a letter or number.
        - Contain only letters numbers, or underscores.
        """
        v = v.lower()
        
        regex = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_]{4,31}$")
        if not regex.match(v):
            raise GeneralErrorReponses.bad_format("username")
        
        return v
    
    @field_validator("password", mode="after")
    def validate_password(cls, v: str) -> str:
        """
        - 8 to 40 characters.
        - Atleast contain 1 number.
        - Atleast contain 1 letter.

        """
        regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,50}$")
        if not regex.match(v):
            raise GeneralErrorReponses.bad_format("password")
        
        return v
    
    @field_validator("phone_number", mode="after")
    def validate_phone_number(cls, v: str) -> str:
        """
        - All need to be number.
        - Start wiht 09.
        - length excactly be 11.
        """
        regex = re.compile(r"^09\d{9}$")
        if not regex.match(v):
            raise GeneralErrorReponses.bad_format("phone number")
        
        return v
    
class UserOut(BaseModel):
    id: int
    username: str
    phone_number: str
    email: str | None
    role: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    
class UserTokenOut(UserOut, TokenOut):
    pass