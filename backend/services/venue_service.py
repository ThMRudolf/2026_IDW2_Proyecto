import math

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Venue


def get_venues(db: Session, page: int, limit: int):
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
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
