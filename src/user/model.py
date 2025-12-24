from enum import Enum

from sqlalchemy import Column ,String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy import Enum as AlchemyEnum
from sqlalchemy.orm import relationship

from src.core.model import Base
from src.core.model import UserRole


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    email = Column(String(254), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    email_approved = Column(Boolean, nullable=False, default=False)
    
    role = Column(AlchemyEnum(UserRole, name="user_role", native_enum=True), nullable=False, default=UserRole.user)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    profile = relationship("Profile", back_populates="user")
    cafe_comments = relationship("CafeComment", back_populates="user")
    own_cafes = relationship("Cafe", back_populates="owner")
    
    
    
class Profile(Base):
    __tablename__ = "profile"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), unique=True, index=True)
    user = relationship("User", back_populates="profile")
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    anonymous = Column(Boolean, nullable=False, default=True)