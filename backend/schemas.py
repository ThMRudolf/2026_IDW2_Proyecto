"""
Pydantic schemas for request validation and response serialisation.

Objective:
    Define the data contracts between the HTTP layer and the service layer.
    Each domain has three schema roles:
      - Create  : validates incoming POST/PUT body fields.
      - Update  : validates incoming PATCH body fields (all fields optional).
      - Read    : serialises ORM instances into JSON responses.

    PaginatedResponse[T] is a generic envelope used by every list endpoint.

Schemas defined:
    PaginatedResponse[T]  -- Generic pagination envelope.
    StoryCreate           -- Input for creating a story.
    StoryUpdate           -- Input for partially updating a story.
    StoryRead             -- Output for a single story.
    StandingRead          -- Output for a single standing row.
    VenueRead             -- Output for a single venue.
    CountryRead           -- Output for a single host country.
    InstagramPostRead     -- Output for a single feed post.
    UserCreate            -- Input for registering a user.
    UserRead              -- Output for a single user.
"""

from __future__ import annotations
from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, HttpUrl

T = TypeVar("T")


# ── Pagination envelope ────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic pagination envelope returned by all list endpoints.

    Fields:
        items (List[T]) -- Records on the current page.
        total (int)     -- Total number of records matching the query.
        page  (int)     -- Current 1-based page number.
        limit (int)     -- Page size used for this response.
        pages (int)     -- Total number of available pages.
    """
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int

    class Config:
        from_attributes = True


# ── Stories ────────────────────────────────────────────────────────────────────

class StoryCreate(BaseModel):
    """
    Input schema for creating or fully replacing a story (POST / PUT).

    Fields:
        title     (str)     -- Story headline.
        section   (str)     -- Content category (e.g. "match", "opinion").
        body      (str)     -- Full article body.
        image_url (HttpUrl) -- Validated URL to the story's cover image.
    """
    title: str
    section: str
    body: str
    image_url: HttpUrl


class StoryUpdate(BaseModel):
    """
    Input schema for partially updating a story (PATCH).

    All fields are optional; only supplied fields are applied.

    Fields:
        title     (Optional[str])     -- New headline, if changing.
        section   (Optional[str])     -- New section label, if changing.
        body      (Optional[str])     -- New body text, if changing.
        image_url (Optional[HttpUrl]) -- New cover image URL, if changing.
    """
    title: Optional[str] = None
    section: Optional[str] = None
    body: Optional[str] = None
    image_url: Optional[HttpUrl] = None


class StoryRead(BaseModel):
    """
    Output schema for serialising a Story ORM instance.

    Fields:
        id         (int)      -- Unique story identifier.
        title      (str)      -- Story headline.
        section    (str)      -- Content category.
        body       (str)      -- Full article body.
        image_url  (str)      -- Cover image URL.
        user_id    (str)      -- x_user_id of the author.
        created_at (datetime) -- UTC creation timestamp.
        updated_at (datetime) -- UTC last-modified timestamp.
    """
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
    """
    Output schema for serialising a Standing ORM instance.

    Fields:
        id         (int) -- Unique standing identifier.
        group_name (str) -- Group label (e.g. "A", "B").
        team       (str) -- Team name.
        flag_url   (str) -- URL to the team's flag image.
        played     (int) -- Matches played.
        wins       (int) -- Matches won.
        draws      (int) -- Matches drawn.
        losses     (int) -- Matches lost.
        points     (int) -- Accumulated points.
    """
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
    """
    Output schema for serialising a Venue ORM instance.

    Fields:
        id              (int) -- Unique venue identifier.
        name            (str) -- Stadium name.
        city            (str) -- City where the stadium is located.
        capacity        (int) -- Maximum spectator capacity.
        image_url       (str) -- URL to the stadium's photo.
        host_country_id (int) -- Foreign key to the hosting country.
    """
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
    """
    Output schema for serialising a HostCountry ORM instance.

    Fields:
        id          (int) -- Unique country identifier.
        name        (str) -- Country name.
        flag_url    (str) -- URL to the country's flag image.
        description (str) -- Short editorial description.
        continent   (str) -- Continent the country belongs to.
    """
    id: int
    name: str
    flag_url: str
    description: str
    continent: str

    class Config:
        from_attributes = True


# ── Instagram Feed ─────────────────────────────────────────────────────────────

class InstagramPostRead(BaseModel):
    """
    Output schema for serialising an InstagramPost ORM instance.

    Fields:
        id        (int)      -- Unique post identifier.
        image_url (str)      -- URL to the post's image.
        caption   (str)      -- Short caption shown beneath the image.
        link      (str)      -- External URL the post links to.
        posted_at (datetime) -- UTC timestamp when the post was published.
    """
    id: int
    image_url: str
    caption: str
    link: str
    posted_at: datetime

    class Config:
        from_attributes = True


# ── Users ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """
    Input schema for registering a new user (POST /api/users).

    Fields:
        username (str) -- Desired display name.
        email    (str) -- User's email address (must be unique in the database).
    """
    username: str
    email: str


class UserRead(BaseModel):
    """
    Output schema for serialising a User ORM instance.

    Fields:
        id         (int)      -- Unique user identifier.
        username   (str)      -- Display name.
        email      (str)      -- Email address.
        x_user_id  (str)      -- UUID token the frontend stores in
                                 sessionStorage for subsequent requests.
        created_at (datetime) -- UTC timestamp of account creation.
    """
    id: int
    username: str
    email: str
    x_user_id: str          # frontend stores this in sessionStorage
    created_at: datetime

    class Config:
        from_attributes = True
