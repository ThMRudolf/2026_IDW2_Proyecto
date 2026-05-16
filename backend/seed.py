"""
Database seed script for development and testing.

Objective:
    Populate the database with initial fixture data so the application
    can be run and tested locally without manual data entry.
    Run this script once after the database has been created:

        python seed.py

    Re-running is safe only if existing rows are cleared first; otherwise
    unique-constraint violations will abort the insert.

    NOTE: The ORM model definitions below mirror a subset of models.py.
    They are kept here so the seed script can be executed standalone
    without importing the full application stack.

Inputs:
    None. Reads DATABASE_URL from the environment (via database.py) to
    determine which database to populate.

Output:
    Rows inserted into the stories and standings tables and committed to
    the database. Prints a confirmation message on success.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base


class Story(Base):
    """
    Minimal Story model used by the seed script.

    Mirrors the stories table definition in models.py.
    See models.Story for the full column documentation.
    """
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
    """
    Minimal Standing model used by the seed script.

    Mirrors the standings table definition in models.py.
    See models.Standing for the full column documentation.
    """
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
