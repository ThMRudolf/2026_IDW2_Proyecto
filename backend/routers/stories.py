from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from database import get_db
from schemas import StoryCreate, StoryUpdate, StoryRead, PaginatedResponse
from services import story_service

router = APIRouter(prefix="/api/stories", tags=["stories"])


@router.get("", response_model=PaginatedResponse[StoryRead])
def list_stories(
    page: int = 1,
    limit: int = 10,
    since: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    return story_service.get_stories(db, None, page, limit, since)


@router.get("/{story_id}", response_model=StoryRead)
def get_story(
    story_id: int,
    db: Session = Depends(get_db),
):
    return story_service.get_story_by_id(db, story_id)


@router.post("", response_model=StoryRead, status_code=201)
def create_story(
    payload: StoryCreate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    return story_service.create_story(db, payload, x_user_id)


@router.patch("/{story_id}", response_model=StoryRead)
def patch_story(
    story_id: int,
    payload: StoryUpdate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    return story_service.update_story(db, story_id, payload, x_user_id)


@router.put("/{story_id}", response_model=StoryRead)
def replace_story(
    story_id: int,
    payload: StoryCreate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    return story_service.replace_story(db, story_id, payload, x_user_id)


@router.delete("/{story_id}", status_code=204)
def delete_story(
    story_id: int,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    story_service.delete_story(db, story_id, x_user_id)
