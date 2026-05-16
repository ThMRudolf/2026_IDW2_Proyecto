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
    return country_service.get_countries(db, page, limit)


@router.get("/{country_id}", response_model=CountryRead)
def get_country(
    country_id: int,
    db: Session = Depends(get_db),
):
    return country_service.get_country_by_id(db, country_id)
