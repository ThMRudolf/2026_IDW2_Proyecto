from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(100), nullable=False)
    email       = Column(String(255), nullable=False, unique=True)
    x_user_id   = Column(String(36), nullable=False, unique=True, index=True)
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)


class Story(Base):
    __tablename__ = "stories"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False)
    section    = Column(String(100), nullable=False)
    body       = Column(Text, nullable=False)
    image_url  = Column(String(500), nullable=False)
    user_id    = Column(String(36), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Standing(Base):
    __tablename__ = "standings"

    id         = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(10), nullable=False, index=True)
    team       = Column(String(100), nullable=False)
    flag_url   = Column(String(500), nullable=False)
    played     = Column(Integer, default=0)
    wins       = Column(Integer, default=0)
    draws      = Column(Integer, default=0)
    losses     = Column(Integer, default=0)
    points     = Column(Integer, default=0)


class HostCountry(Base):
    __tablename__ = "host_countries"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    flag_url    = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    continent   = Column(String(50), nullable=False)


class Venue(Base):
    __tablename__ = "venues"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(200), nullable=False)
    city            = Column(String(100), nullable=False)
    capacity        = Column(Integer, nullable=False)
    image_url       = Column(String(500), nullable=False)
    host_country_id = Column(Integer, ForeignKey("host_countries.id"), nullable=False)


class InstagramPost(Base):
    __tablename__ = "instagram_feed"

    id        = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    caption   = Column(String(300), nullable=False)
    link      = Column(String(500), nullable=False)
    posted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
