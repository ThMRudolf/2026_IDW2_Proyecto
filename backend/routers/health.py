from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import httpx

router = APIRouter(prefix="/api/external", tags=["external"])
# routers/health.py
@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
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