"""
Application entry point for the FIFA 2026 API.

Objective:
    Bootstrap the FastAPI application: create all database tables, configure
    CORS so the React frontend can reach the API, and register every router
    under its declared prefix.

Environment variables:
    ALLOWED_ORIGINS (str, default "http://localhost:5173") -- Comma-separated
        list of origins that the browser is permitted to call. Set to the
        production frontend URL(s) before deploying.

Registered routers and prefixes:
    /health            -- Liveness / readiness probe.
    /api/users         -- User registration and lookup.
    /api/stories       -- Fan-authored story CRUD.
    /api/standings     -- Tournament group-stage standings.
    /api/venues        -- Stadium information.
    /api/countries     -- Host-country information.
    /api/instagram     -- Instagram-style post feed.
    /api/external      -- Proxied data from API-Football v3.

Notes:
    Tables are created via Base.metadata.create_all on every startup.
    For production use Alembic migrations instead.
"""

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
