"""
Router for endpoints that proxy third-party sports data APIs.

All routes are prefixed with /api/external and tagged "external" in the
OpenAPI schema.
"""

from fastapi import APIRouter, Query
from services import external_api_service
from dotenv import load_dotenv
import os

load_dotenv()

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
router = APIRouter(prefix="/api/external", tags=["external"])


@router.get("/topscorers")
async def get_topscorers(
    league: int = Query(default=1, description="API-Football league id"),
    season: int = Query(default=2026, description="Season year"),
):
    """Return the top goal-scorers for a given league and season.

    Proxies the API-Football ``/players/topscorers`` endpoint and returns a
    trimmed-down list containing only the fields the frontend requires.

    **Query parameters**

    | Name     | Type | Default | Description                     |
    |----------|------|---------|---------------------------------|
    | league   | int  | 1       | API-Football numeric league id  |
    | season   | int  | 2026    | Four-digit season year          |

    **Response** — ``200 OK`` — list of scorer objects:

    ```json
    [
      {
        "id":             39,
        "name":           "L. Messi",
        "avatar_url":     "https://…/photo.png",
        "team":           "Inter Miami",
        "team_logo":      "https://…/logo.png",
        "league":         "Major League Soccer",
        "goals":          18,
        "assists":        12,
        "matches_played": 24
      }
    ]
    ```

    **Error responses**

    | Status | Meaning                                      |
    |--------|----------------------------------------------|
    | 503    | ``API_FOOTBALL_KEY`` environment var not set |
    | 502    | Upstream API returned an error or is down    |
    | 504    | Upstream API request timed out (> 10 s)      |
    """
    return await external_api_service.get_topscorers(league, season)
