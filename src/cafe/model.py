from sqlalchemy import Column, String, Integer, Float, Text, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as AlchemyEnum
from geoalchemy2 import Geometry

from src.core.model import Base, CommentRole, Provider, SchedulDays

class Cafe(Base):
    __tablename__ = "cafe"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    
    name = Column(String(200), nullable=False)
    aboute = Column(Text, nullable=True)
    geom = Column(Geometry(geometry_type="POINT", srid=4326))
    rate = Column(Float, nullable=False)
    avatar = Column(String(200), nullable=True)
    addres = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(200), nullable=True)

    provider = Column(AlchemyEnum(Provider, name="provider_type", native_enum=True), nullable=False)
    out_source_pk = Column(String(100), nullable=False)

    comments = relationship("CafeComment", back_populates="cafe") 
    cafe_scheduls = relationship("CafeSchedul", back_populates="cafe")


class CafeComment(Base):
    __tablename__ = "cafe_comment"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    
    subject = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    rate = Column(Integer, nullable=True)
    role = Column(AlchemyEnum(CommentRole, name="comment_role", native_enum=True), nullable=False, default=CommentRole.customer)
    anonymous = Column(Boolean, default=True)
    provider = Column(String(100), nullable=False)
    out_source_pk = Column(String(100), nullable=False)

    cafe_id = Column(Integer, ForeignKey("cafe.id", ondelete="CASCADE"), nullable=False, index=True)
    cafe = relationship("Cafe", back_populates="comments")
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="cafe_comments")

    # need reply on comment
    # comment_id = 


class CafeSchedul(Base):
    __tablename__ = "cafe_schedul"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    weekday = Column(AlchemyEnum(SchedulDays, name="schedul_days", native_enum=True), nullable=False, default=SchedulDays.all)
    all_day = Column(Boolean, nullable=False)
    start_hour = Column(Time, nullable=False)
    stop_hour = Column(Time, nullable=False)

    cafe_id = Column(Integer, ForeignKey("cafe.id", ondelete="CASCADE"), nullable=False, index=True)
    cafe = relationship("Cafe", back_populates="cafe_scheduls")