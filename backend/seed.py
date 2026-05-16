from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class Story(Base):
    __tablename__ = "stories"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False)
    section    = Column(String(100), nullable=False)
    body       = Column(Text, nullable=False)
    image_url  = Column(String(500), nullable=False)
    user_id    = Column(String(36), nullable=False, index=True)  # UUID from header
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Standing(Base):
    __tablename__ = "standings"

    id         = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(10), nullable=False, index=True)  # "A", "B", etc.
    team       = Column(String(100), nullable=False)
    flag_url   = Column(String(500), nullable=False)
    played     = Column(Integer, default=0)
    wins       = Column(Integer, default=0)
    draws      = Column(Integer, default=0)
    losses     = Column(Integer, default=0)
    points     = Column(Integer, default=0)
