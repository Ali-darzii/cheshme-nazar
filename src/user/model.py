from sqlmodel import Enum, SQLModel, Field
from sqlalchemy import Column, DateTime, func
from datetime import datetime


class UserRole(int, Enum):
    user = 0
    admin = 1

class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: int = Field(nullable=False, primary_key=True, index=True)
    
    username: str = Field(nullable=False, index=True, max_length=50, unique=True)
    phone_number: str = Field(nullable=False, index=True, max_length=11, unique=True)
    password: str = Field(nullable=False, max_length=128)
    
    is_deleted: bool = Field(default=False, nullable=False)
    email: str | None = Field(nullable=True)
    role: int = Field(default=UserRole.user)
    is_active: bool = Field(default=True, nullable=False)
    phone_approved: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))