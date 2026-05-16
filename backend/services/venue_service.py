"""
Service layer for stadium/venue data access.

Encapsulates all database queries related to Venue records and raises
HTTP exceptions so routers stay free of business logic.
"""

import math

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Venue


def get_venues(db: Session, page: int, limit: int):
    """
    Retrieve a paginated list of venues ordered alphabetically by name.

    Objective:
        Query all Venue rows and return a pagination envelope with the
        requested slice, sorted by name.

    Inputs:
        db    (Session) -- Active SQLAlchemy database session.
        page  (int)     -- 1-based page number.
        limit (int)     -- Maximum number of records per page.

    Output (dict):
        items (List[Venue]) -- Venues on the requested page.
        total (int)         -- Total number of venues in the database.
        page  (int)         -- Current page number.
        limit (int)         -- Page size used for this response.
        pages (int)         -- Total number of available pages.
    """
    query = db.query(Venue)

    total = query.count()
    items = (
        query
        .order_by(Venue.name)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if total else 1,
    }


def get_venue_by_id(db: Session, venue_id: int) -> Venue:
    """
    Retrieve a single venue by its primary key.

    Objective:
        Look up one Venue record and raise a 404 if it does not exist.

    Inputs:
        db       (Session) -- Active SQLAlchemy database session.
        venue_id (int)     -- Primary key of the venue to retrieve.

    Output (Venue):
        The matching Venue ORM instance.

    Raises:
        HTTPException 404 -- If no venue with the given ID exists.
    """
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
