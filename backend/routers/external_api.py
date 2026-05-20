# routers/external_api.py
import os
import httpx
from fastapi import APIRouter, Query
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/external", tags=["External APIs"])

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_FOOTBALL_KEY:
    raise ValueError("API_FOOTBALL_KEY not configured in environment")


@router.get("/topscorers")
async def get_topscorers(
    league: int = Query(default=1, description="API-Football league id"),
    season: int = Query(default=2026, description="Season year"),
):
    """
    Get top scorers for a league and season from API Football
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
    
    headers = {
        "x-rapidapi-key": API_FOOTBALL_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    
    params = {
        "league": league,
        "season": season
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPStatusError as e:
        return {
            "error": f"API Football returned {e.status_code}",
            "details": str(e.response.text) if hasattr(e.response, 'text') else None
        }
    except httpx.TimeoutException:
        return {"error": "API Football request timeout"}
    except Exception as e:
        return {"error": str(e)}
