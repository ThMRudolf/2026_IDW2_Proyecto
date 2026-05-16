from __future__ import annotations
from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, HttpUrl

T = TypeVar("T")


# ── Pagination envelope ────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int

    class Config:
        from_attributes = True


# ── Stories ────────────────────────────────────────────────────────────────────

class StoryCreate(BaseModel):
    title: str
    section: str
    body: str
    image_url: HttpUrl


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    section: Optional[str] = None
    body: Optional[str] = None
    image_url: Optional[HttpUrl] = None


class StoryRead(BaseModel):
    id: int
    title: str
    section: str
    body: str
    image_url: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Standings ──────────────────────────────────────────────────────────────────

class StandingRead(BaseModel):
    id: int
    group_name: str
    team: str
    flag_url: str
    played: int
    wins: int
    draws: int
    losses: int
    points: int

    class Config:
        from_attributes = True


# ── Venues ─────────────────────────────────────────────────────────────────────

class VenueRead(BaseModel):
    id: int
    name: str
    city: str
    capacity: int
    image_url: str
    host_country_id: int

    class Config:
        from_attributes = True


# ── Host Countries ─────────────────────────────────────────────────────────────

class CountryRead(BaseModel):
    id: int
    name: str
    flag_url: str
    description: str
    continent: str

    class Config:
        from_attributes = True


# ── Instagram Feed ─────────────────────────────────────────────────────────────

class InstagramPostRead(BaseModel):
    id: int
    image_url: str
    caption: str
    link: str
    posted_at: datetime

    class Config:
        from_attributes = True


# ── Users ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    x_user_id: str          # frontend stores this in sessionStorage
    created_at: datetime

    class Config:
        from_attributes = True
