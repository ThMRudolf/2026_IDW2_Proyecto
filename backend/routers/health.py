"""
Router for application health-check endpoints.

Reports the liveness status of the API server and its dependencies
(database and API-Football upstream). Intended for use by load balancers,
container orchestrators, and monitoring dashboards.
Route: GET /api/external/health
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import httpx

router = APIRouter(prefix="/api/external", tags=["external"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Check the health of the API and its upstream dependencies.

    Objective:
        Verify that the database is reachable and that the API-Football
        upstream service is responding. Returns a combined status so
        monitoring tools can detect partial degradation.

    Inputs:
        None -- no query parameters or request body required.

    Output (JSON object):
        status      (str)  -- "ok" if the database is healthy, "degraded" otherwise.
        db          (str)  -- "ok" if the database responds to a ping, "error" otherwise.
        api_football (str) -- "ok" if API-Football /status returns 200, "error" otherwise.
        timestamp   (str)  -- ISO-8601 UTC timestamp of when the check was performed.

    HTTP status codes:
        200 -- Always returned (even when dependencies are degraded), so that
               load balancers receive a response. Callers must inspect the body
               to determine actual health.
    """
    # 1. Verificar DB
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    # 2. Verificar API-Football
    try:
        r = await httpx.AsyncClient().get(
            "https://v3.football.api-sports.io/status",
            headers={"x-apisports-key": API_FOOTBALL_KEY},
            timeout=5.0
        )
        api_status = "ok" if r.status_code == 200 else "error"
    except Exception:
        api_status = "error"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status,
        "api_football": api_status,
        "timestamp": datetime.utcnow().isoformat()
    }
