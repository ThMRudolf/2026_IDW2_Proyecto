from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import InstagramPostRead, PaginatedResponse
from services import instagram_service

router = APIRouter(prefix="/api/instagram", tags=["instagram"])


@router.get("/feed", response_model=PaginatedResponse[InstagramPostRead])
def get_feed(
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
):
    return instagram_service.get_feed(db, page, limit)
