import math

from sqlalchemy.orm import Session

from models import InstagramPost


def get_feed(db: Session, page: int, limit: int):
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
