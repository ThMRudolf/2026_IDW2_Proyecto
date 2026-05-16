from fastapi import APIRouter, Query
from services import external_api_service

router = APIRouter(prefix="/api/external", tags=["external"])


@router.get("/topscorers")
async def get_topscorers(
    league: int = Query(default=1, description="API-Football league id"),
    season: int = Query(default=2026, description="Season year"),
):
    return await external_api_service.get_topscorers(league, season)
