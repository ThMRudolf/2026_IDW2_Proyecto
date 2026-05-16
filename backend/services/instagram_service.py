"""
Service layer for the Instagram-style post feed.

Encapsulates all database queries related to InstagramPost records,
returning posts ordered from newest to oldest with pagination support.
"""

import math

from sqlalchemy.orm import Session

from models import InstagramPost


def get_feed(db: Session, page: int, limit: int):
    """
    Retrieve a paginated feed of Instagram posts ordered newest-first.

    Objective:
        Query all InstagramPost rows sorted by posted_at descending and
        return a pagination envelope with the requested slice.

    Inputs:
        db    (Session) -- Active SQLAlchemy database session.
        page  (int)     -- 1-based page number.
        limit (int)     -- Maximum number of records per page.

    Output (dict):
        items (List[InstagramPost]) -- Posts on the requested page.
        total (int)                 -- Total number of posts in the database.
        page  (int)                 -- Current page number.
        limit (int)                 -- Page size used for this response.
        pages (int)                 -- Total number of available pages.
    """
    query = db.query(InstagramPost)

    total = query.count()
    items = (
        query
        .order_by(InstagramPost.posted_at.desc())
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
