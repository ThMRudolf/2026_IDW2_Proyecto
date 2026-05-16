"""
Router for tournament venue endpoints.

Provides read-only access to stadium and venue data with pagination support.
All routes are prefixed with /api/venues.
"""

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
    """
    Retrieve a paginated list of tournament venues.

    Objective:
        Return all stadiums and venues that host tournament matches,
        split into pages.

    Inputs (query params):
        page  (int, default=1)  -- 1-based page number to retrieve.
        limit (int, default=10) -- Maximum number of venues per page.

    Output (PaginatedResponse[VenueRead]):
        items (List[VenueRead]) -- Venues on the requested page. Each entry contains:
            id              (int) -- Unique venue identifier.
            name            (str) -- Venue name.
            city            (str) -- City where the venue is located.
            capacity        (int) -- Maximum spectator capacity.
            image_url       (str) -- URL of the venue photo.
            host_country_id (int) -- Foreign key referencing the host country.
        total (int) -- Total number of venues in the database.
        page  (int) -- Current page number.
        limit (int) -- Page size used for this response.
        pages (int) -- Total number of available pages.
    """
    return venue_service.get_venues(db, page, limit)


@router.get("/{venue_id}", response_model=VenueRead)
def get_venue(
    venue_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single venue by its ID.

    Objective:
        Return the full details of one venue identified by its primary key.

    Inputs (path param):
        venue_id (int) -- Primary key of the venue to retrieve.

    Output (VenueRead):
        id              (int) -- Unique venue identifier.
        name            (str) -- Venue name.
        city            (str) -- City where the venue is located.
        capacity        (int) -- Maximum spectator capacity.
        image_url       (str) -- URL of the venue photo.
        host_country_id (int) -- Foreign key referencing the host country.

    Raises:
        404 Not Found -- If no venue with the given ID exists.
    """
    return venue_service.get_venue_by_id(db, venue_id)
