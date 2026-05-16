import math

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import HostCountry


def get_countries(db: Session, page: int, limit: int):
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
    country = db.query(HostCountry).filter(HostCountry.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country
