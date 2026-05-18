from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from math import ceil

from database import get_db
from models import InstagramPost

router = APIRouter(prefix="/api/instagram", tags=["instagram"])


@router.get("")
def list_instagram_posts(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(InstagramPost).order_by(InstagramPost.id.desc())

    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": ceil(total / limit) if total else 1,
    }


@router.get("/{post_id}")
def get_instagram_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Instagram post not found")

    return post