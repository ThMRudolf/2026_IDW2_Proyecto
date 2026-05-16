"""
Service layer for host-country data access.

Encapsulates all database queries related to HostCountry records and
raises HTTP exceptions so routers stay free of business logic.
"""

import math

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import HostCountry


def get_countries(db: Session, page: int, limit: int):
    """
    Retrieve a paginated list of host countries ordered alphabetically.

    Objective:
        Query all HostCountry rows and return a pagination envelope with
        the requested slice, sorted by name.

    Inputs:
        db    (Session) -- Active SQLAlchemy database session.
        page  (int)     -- 1-based page number.
        limit (int)     -- Maximum number of records per page.

    Output (dict):
        items (List[HostCountry]) -- Countries on the requested page.
        total (int)               -- Total number of countries in the database.
        page  (int)               -- Current page number.
        limit (int)               -- Page size used for this response.
        pages (int)               -- Total number of available pages.
    """
    query = db.query(HostCountry)

    total = query.count()
    items = (
        query
        .order_by(HostCountry.name)
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


def get_country_by_id(db: Session, country_id: int) -> HostCountry:
    """
    Retrieve a single host country by its primary key.

    Objective:
        Look up one HostCountry record and raise a 404 if it does not exist.

    Inputs:
        db         (Session) -- Active SQLAlchemy database session.
        country_id (int)     -- Primary key of the country to retrieve.

    Output (HostCountry):
        The matching HostCountry ORM instance.

    Raises:
        HTTPException 404 -- If no country with the given ID exists.
    """
    country = db.query(HostCountry).filter(HostCountry.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
