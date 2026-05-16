"""
SQLAlchemy ORM models for the FIFA 2026 API.

Objective:
    Define the database schema as Python classes that map directly to
    relational tables. All classes inherit from Base (declarative_base)
    so SQLAlchemy can auto-create and migrate tables.

Tables defined:
    users          -- Registered application users.
    stories        -- Fan-authored content entries.
    standings      -- Group-stage tournament standings.
    host_countries -- Countries hosting the tournament.
    venues         -- Stadiums / match venues.
    instagram_feed -- Instagram-style curated post feed.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class User(Base):
    """
    Represents a registered application user.

    Columns:
        id         (Integer, PK)     -- Auto-incremented primary key.
        username   (String 100)      -- Display name chosen by the user.
        email      (String 255, UQ)  -- Unique email address.
        x_user_id  (String 36, UQ)   -- UUID token issued at signup;
                                        stored by the client for auth.
        created_at (DateTime)        -- UTC timestamp of account creation.
    """
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(100), nullable=False)
    email       = Column(String(255), nullable=False, unique=True)
    x_user_id   = Column(String(36), nullable=False, unique=True, index=True)
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)


class Story(Base):
    """
    Fan-authored content entry (article / match report / opinion).

    Columns:
        id         (Integer, PK)   -- Auto-incremented primary key.
        title      (String 255)    -- Headline of the story.
        section    (String 100)    -- Content category (e.g. "match", "opinion").
        body       (Text)          -- Full article body.
        image_url  (String 500)    -- URL to the story's cover image.
        user_id    (String 36, IX) -- x_user_id of the author; not a FK so
                                      users can be deleted without cascade.
        created_at (DateTime)      -- UTC timestamp of creation.
        updated_at (DateTime)      -- UTC timestamp of last modification.
    """
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
    """
    One team's statistics within a tournament group.

    Columns:
        id         (Integer, PK)    -- Auto-incremented primary key.
        group_name (String 10, IX)  -- Group label (e.g. "A", "B").
        team       (String 100)     -- Team name.
        flag_url   (String 500)     -- URL to the team's flag image.
        played     (Integer)        -- Matches played.
        wins       (Integer)        -- Matches won.
        draws      (Integer)        -- Matches drawn.
        losses     (Integer)        -- Matches lost.
        points     (Integer)        -- Accumulated points.
    """
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
    """
    A country that is co-hosting the 2026 FIFA World Cup.

    Columns:
        id          (Integer, PK) -- Auto-incremented primary key.
        name        (String 100)  -- Country name.
        flag_url    (String 500)  -- URL to the country's flag image.
        description (Text)        -- Short editorial description.
        continent   (String 50)   -- Continent the country belongs to.
    """
    __tablename__ = "host_countries"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    flag_url    = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    continent   = Column(String(50), nullable=False)


class Venue(Base):
    """
    A stadium or match venue used during the tournament.

    Columns:
        id              (Integer, PK) -- Auto-incremented primary key.
        name            (String 200)  -- Stadium name.
        city            (String 100)  -- City where the stadium is located.
        capacity        (Integer)     -- Maximum spectator capacity.
        image_url       (String 500)  -- URL to the stadium's photo.
        host_country_id (Integer, FK) -- Foreign key to host_countries.id.
    """
    __tablename__ = "venues"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(200), nullable=False)
    city            = Column(String(100), nullable=False)
    capacity        = Column(Integer, nullable=False)
    image_url       = Column(String(500), nullable=False)
    host_country_id = Column(Integer, ForeignKey("host_countries.id"), nullable=False)


class InstagramPost(Base):
    """
    A curated post displayed in the Instagram-style feed.

    Columns:
        id        (Integer, PK) -- Auto-incremented primary key.
        image_url (String 500)  -- URL to the post's image.
        caption   (String 300)  -- Short caption shown beneath the image.
        link      (String 500)  -- External URL the post links to.
        posted_at (DateTime)    -- UTC timestamp when the post was published.
    """
    __tablename__ = "instagram_feed"

    id        = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    caption   = Column(String(300), nullable=False)
    link      = Column(String(500), nullable=False)
    posted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
