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
    standing = db.query(Standing).filter(Standing.id == standing_id).first()
    if not standing:
        raise HTTPException(status_code=404, detail="Standing not found")
    return standing
