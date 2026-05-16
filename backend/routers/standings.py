from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas import StandingRead, PaginatedResponse
from services import standings_service

router = APIRouter(prefix="/api/standings", tags=["standings"])


@router.get("", response_model=PaginatedResponse[StandingRead])
def list_standings(
    page: int = 1,
    limit: int = 10,
    group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return standings_service.get_standings(db, page, limit, group)


@router.get("/{standing_id}", response_model=StandingRead)
def get_standing(
    standing_id: int,
    db: Session = Depends(get_db),
):
    return standings_service.get_standing_by_id(db, standing_id)
