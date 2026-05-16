"""
Router for tournament standings endpoints.

Provides read-only access to group-stage standings with optional group
filtering and pagination support.
All routes are prefixed with /api/standings.
"""

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
    """
    Retrieve a paginated list of tournament standings, optionally filtered by group.

    Objective:
        Return the current standings table for all groups, or for a single
        group when the group filter is provided.

    Inputs (query params):
        page  (int, default=1)          -- 1-based page number to retrieve.
        limit (int, default=10)         -- Maximum number of entries per page.
        group (str, optional, default=None) -- Group name to filter by (e.g. "A", "B").
                                              When omitted all groups are returned.

    Output (PaginatedResponse[StandingRead]):
        items (List[StandingRead]) -- Standings on the requested page. Each entry contains:
            id         (int) -- Unique standing row identifier.
            group_name (str) -- Name of the group (e.g. "A").
            team       (str) -- Team name.
            flag_url   (str) -- URL to the team / country flag image.
            played     (int) -- Number of matches played.
            wins       (int) -- Number of wins.
            draws      (int) -- Number of draws.
            losses     (int) -- Number of losses.
            points     (int) -- Accumulated points.
        total (int) -- Total number of standing rows matching the filter.
        page  (int) -- Current page number.
        limit (int) -- Page size used for this response.
        pages (int) -- Total number of available pages.
    """
    return standings_service.get_standings(db, page, limit, group)


@router.get("/{standing_id}", response_model=StandingRead)
def get_standing(
    standing_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single standing row by its ID.

    Objective:
        Return the full standing details of one row identified by its primary key.

    Inputs (path param):
        standing_id (int) -- Primary key of the standing row to retrieve.

    Output (StandingRead):
        id         (int) -- Unique standing row identifier.
        group_name (str) -- Name of the group (e.g. "A").
        team       (str) -- Team name.
        flag_url   (str) -- URL to the team / country flag image.
        played     (int) -- Number of matches played.
        wins       (int) -- Number of wins.
        draws      (int) -- Number of draws.
        losses     (int) -- Number of losses.
        points     (int) -- Accumulated points.

    Raises:
        404 Not Found -- If no standing row with the given ID exists.
    """
    return standings_service.get_standing_by_id(db, standing_id)
