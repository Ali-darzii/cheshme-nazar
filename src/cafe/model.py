from sqlalchemy import Column, String, Integer, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as AlchemyEnum
from geoalchemy2 import Geometry

from src.core.model import Base, CommentRole

class Cafe(Base):
    __tablename__ = "cafe"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    
    name = Column(String(200), nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    rate = Column(Float, nullable=False)
    avatar = Column(String(200), nullable=True)
    aboute = Column(Text, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    owner = relationship("User", back_populates="cafes")
    
    comments = relationship("CafeComment", back_populates="cafe") 
    
class CafeComment(Base):
    __tablename__ = "cafe_comment"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    
    subject = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    rate = Column(Integer, nullable=False)
    role = Column(AlchemyEnum(CommentRole, name="comment_role", native_enum=True), nullable=False, default=CommentRole.customer)
    anonymous = Column(Boolean, default=True)
    
    cafe_id = Column(Integer, ForeignKey("cafe.id", ondelete="CASCADE"), nullable=False, index=True)
    cafe = relationship("Cafe", back_populates="comments")
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="cafe_comments")