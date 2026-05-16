import os

import httpx
from fastapi import HTTPException

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"


def _transform_scorer(raw: dict) -> dict:
    """Keep only the fields the frontend needs. Isolates us from API changes."""
    player = raw.get("player", {})
    stats = raw.get("statistics", [{}])[0]

    return {
        "id":            player.get("id"),
        "name":          player.get("name"),
        "avatar_url":    player.get("photo"),
        "team":          stats.get("team", {}).get("name"),
        "team_logo":     stats.get("team", {}).get("logo"),
        "league":        stats.get("league", {}).get("name"),
        "goals":         stats.get("goals", {}).get("total", 0),
        "assists":       stats.get("goals", {}).get("assists", 0),
        "matches_played": stats.get("games", {}).get("appearences", 0),
    }


async def get_topscorers(league: int, season: int) -> list[dict]:
    if not API_FOOTBALL_KEY:
        raise HTTPException(status_code=503, detail="API_FOOTBALL_KEY not configured")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_FOOTBALL_BASE}/players/topscorers",
                headers={"x-apisports-key": API_FOOTBALL_KEY},
                params={"league": league, "season": season},
                timeout=10.0,
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="API-Football request timed out")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Could not reach API-Football")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="API-Football returned an error")

    data = response.json()
    scorers = data.get("response", [])

    return [_transform_scorer(s) for s in scorers]
