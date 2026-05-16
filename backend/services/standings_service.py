"""
Service layer for tournament standings data access.

Encapsulates all database queries related to Standing records, including
optional group-stage filtering, and raises HTTP exceptions so routers
stay free of business logic.
"""

import math
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Standing


def get_standings(
    db: Session,
    page: int,
    limit: int,
    group: Optional[str],
):
    """
    Retrieve a paginated list of standings, optionally filtered by group.

    Objective:
        Query Standing rows ordered by group name then points descending.
        When a group label is supplied, only that group's rows are returned.

    Inputs:
        db    (Session)       -- Active SQLAlchemy database session.
        page  (int)           -- 1-based page number.
        limit (int)           -- Maximum number of records per page.
        group (Optional[str]) -- Case-insensitive group label (e.g. "A").
                                 Pass None to return all groups.

    Output (dict):
        items (List[Standing]) -- Standings on the requested page.
        total (int)            -- Total number of matching standings.
        page  (int)            -- Current page number.
        limit (int)            -- Page size used for this response.
        pages (int)            -- Total number of available pages.
    """
    query = db.query(Standing)

    if group:
        query = query.filter(Standing.group_name == group.upper())

    total = query.count()
    items = (
        query
        .order_by(Standing.group_name, Standing.points.desc())
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


def get_standing_by_id(db: Session, standing_id: int) -> Standing:
    """
    Retrieve a single standing row by its primary key.

    Objective:
        Look up one Standing record and raise a 404 if it does not exist.

    Inputs:
        db          (Session) -- Active SQLAlchemy database session.
        standing_id (int)     -- Primary key of the standing to retrieve.

    Output (Standing):
        The matching Standing ORM instance.

    Raises:
        HTTPException 404 -- If no standing with the given ID exists.
    """
    standing = db.query(Standing).filter(Standing.id == standing_id).first()
    if not standing:
        raise HTTPException(status_code=404, detail="Standing not found")
    return standing
