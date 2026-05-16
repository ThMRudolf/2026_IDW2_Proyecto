"""
Service layer for third-party football data (API-Football v3).

Proxies requests to api-sports.io and normalises the response into a
stable shape so the rest of the codebase is isolated from upstream
API changes.  Requires the API_FOOTBALL_KEY environment variable.
"""

import os

import httpx
from fastapi import HTTPException

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"


def _transform_scorer(raw: dict) -> dict:
    """
    Normalise a single raw scorer object from API-Football into a flat dict.

    Objective:
        Extract only the fields the frontend needs and flatten the nested
        structure, so callers are isolated from upstream API changes.

    Inputs:
        raw (dict) -- One element from the API-Football "response" array,
                      containing "player" and "statistics" sub-objects.

    Output (dict):
        id             (int | None) -- Player identifier from API-Football.
        name           (str | None) -- Full player name.
        avatar_url     (str | None) -- URL to the player's photo.
        team           (str | None) -- Name of the player's current team.
        team_logo      (str | None) -- URL to the team's logo.
        league         (str | None) -- Name of the competition.
        goals          (int)        -- Total goals scored (0 if unavailable).
        assists        (int)        -- Total assists (0 if unavailable).
        matches_played (int)        -- Number of appearances (0 if unavailable).
    """
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
    """
    Fetch and normalise the top-scorers list from API-Football.

    Objective:
        Call the /players/topscorers endpoint for the given league and season,
        then transform each entry into a flat dict via _transform_scorer.

    Inputs:
        league (int) -- API-Football league ID.
        season (int) -- Four-digit season year (e.g. 2026).

    Output (list[dict]):
        Ordered list of normalised scorer dicts as returned by _transform_scorer.

    Raises:
        HTTPException 503 -- If API_FOOTBALL_KEY is not configured.
        HTTPException 504 -- If the upstream request times out.
        HTTPException 502 -- If the upstream request fails or returns a non-200 status.
    """
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
