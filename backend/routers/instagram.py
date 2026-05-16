"""
Router for Instagram feed endpoints.

Provides read-only access to curated Instagram posts stored in the database,
with pagination support.
All routes are prefixed with /api/instagram.
"""

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
    """
    Retrieve a paginated list of Instagram posts for the in-app feed.

    Objective:
        Return curated Instagram posts in reverse-chronological order so the
        frontend can render an image feed widget.

    Inputs (query params):
        page  (int, default=1)  -- 1-based page number to retrieve.
        limit (int, default=12) -- Maximum number of posts per page.
                                   Default matches a typical 3-column grid row count.

    Output (PaginatedResponse[InstagramPostRead]):
        items (List[InstagramPostRead]) -- Posts on the requested page. Each entry contains:
            id        (int)      -- Unique post identifier.
            image_url (str)      -- URL of the post image.
            caption   (str)      -- Post caption text.
            link      (str)      -- URL to the original Instagram post.
            posted_at (datetime) -- Publication timestamp (UTC).
        total (int) -- Total number of posts in the database.
        page  (int) -- Current page number.
        limit (int) -- Page size used for this response.
        pages (int) -- Total number of available pages.
    """
    return instagram_service.get_feed(db, page, limit)
