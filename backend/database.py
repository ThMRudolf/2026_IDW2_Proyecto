"""
Database configuration and session management.

Objective:
    Bootstrap the SQLAlchemy engine, session factory, and declarative base
    from environment variables, and expose a FastAPI-compatible dependency
    that provides a per-request database session.

Environment variables:
    DATABASE_URL (str, default "sqlite:///./dev.db") -- SQLAlchemy connection
        string. Supports SQLite for local development and PostgreSQL for
        production. SQLite connections automatically receive the
        check_same_thread=False argument required for multi-threaded use.

Module-level objects:
    engine       (Engine)         -- SQLAlchemy engine bound to DATABASE_URL.
    SessionLocal (sessionmaker)   -- Session factory (autocommit/autoflush off).
    Base         (DeclarativeMeta) -- Base class for all ORM model definitions.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# SQLite needs this extra arg; PostgreSQL ignores it
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session for a single request.

    Objective:
        Open a new SQLAlchemy session at the start of a request and
        guarantee it is closed when the request finishes, regardless of
        whether an exception occurred.

    Inputs:
        None. Intended to be injected via FastAPI's Depends() mechanism.

    Output (Generator[Session, None, None]):
        Yields one Session instance for the duration of the request.
        The session is always closed in the finally block.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
