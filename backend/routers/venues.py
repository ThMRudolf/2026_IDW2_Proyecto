from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import VenueRead, PaginatedResponse
from services import venue_service

router = APIRouter(prefix="/api/venues", tags=["venues"])


@router.get("", response_model=PaginatedResponse[VenueRead])
def list_venues(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return venue_service.get_venues(db, page, limit)


@router.get("/{venue_id}", response_model=VenueRead)
def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
):
    return venue_service.get_venue_by_id(db, venue_id)
