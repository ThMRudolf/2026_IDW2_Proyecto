"""
Router for country-related endpoints.

Provides read-only access to country data with pagination support.
All routes are prefixed with /api/countries.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import CountryRead, PaginatedResponse
from services import country_service

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("", response_model=PaginatedResponse[CountryRead])
def list_countries(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of host countries.

    Objective:
        Return all countries that are hosting the tournament, split into pages.

    Inputs (query params):
        page  (int, default=1)  -- 1-based page number to retrieve.
        limit (int, default=10) -- Maximum number of countries per page.

    Output (PaginatedResponse[CountryRead]):
        items (List[CountryRead]) -- Countries on the requested page. Each entry contains:
            id          (int) -- Unique country identifier.
            name        (str) -- Country name.
            flag_url    (str) -- URL to the country's flag image.
            description (str) -- Short description of the country.
            continent   (str) -- Continent the country belongs to.
        total (int) -- Total number of countries in the database.
        page  (int) -- Current page number.
        limit (int) -- Page size used for this response.
        pages (int) -- Total number of available pages.
    """
    return country_service.get_countries(db, page, limit)


@router.get("/{country_id}", response_model=CountryRead)
def get_country(
    country_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single host country by ID.

    Objective:
        Return the full details of one country identified by its primary key.

    Inputs (path param):
        country_id (int) -- Primary key of the country to retrieve.

    Output (CountryRead):
        id          (int) -- Unique country identifier.
        name        (str) -- Country name.
        flag_url    (str) -- URL to the country's flag image.
        description (str) -- Short description of the country.
        continent   (str) -- Continent the country belongs to.

    Raises:
        404 Not Found -- If no country with the given ID exists.
    """
    return country_service.get_country_by_id(db, country_id)
