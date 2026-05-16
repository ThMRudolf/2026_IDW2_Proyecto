import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import stories, standings, venues, countries, instagram, external_api, users, health

# Create all tables on startup (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FIFA 2026 API",
    description="Backend for the FIFA 2026 World Cup imitation project",
    version="1.0.0",
)

# CORS — allow the React frontend to call this API
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(health.router)
app.include_router(users.router)
app.include_router(stories.router)
app.include_router(standings.router)
app.include_router(venues.router)
app.include_router(countries.router)
app.include_router(instagram.router)
app.include_router(external_api.router)
