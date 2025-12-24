from enum import Enum

from sqlalchemy import Column, String,  Text, Integer, ForeignKey, Boolean
from sqlalchemy import Enum as AlchemyEnum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.inspection import inspect


class UserRole(int, Enum):
    user = 0
    admin = 1
    
    
class CommentRole(int, Enum):
    customer = 0
    employee = 1

class Base(DeclarativeBase):
    
    def model_dump(self,* , exclude_unset=False) -> dict:
        mapper = inspect(self).mapper
        data = {}

        for column in mapper.column_attrs:
            key = column.key
            value = getattr(self, key)
            if exclude_unset and value is None:
                continue

            data[key] = value

        return data

class Comment(Base):
    __abstract__ = True

    subject = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    rate = Column(Integer, nullable=False)
    role = Column(AlchemyEnum(CommentRole, name="comment_role", native_enum=True), nullable=False, default=CommentRole.customer)
    anonymous = Column(Boolean, default=True)
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="cafe_comments")



    