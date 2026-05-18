"""
Service layer for user-authored stories.
"""

import math
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Story
from schemas import StoryCreate, StoryUpdate


def _assert_owner(story: Story, user_id: str):
    if story.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to modify this story",
        )


def _get_or_404(db: Session, story_id: int) -> Story:
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return story


def get_stories(
    db: Session,
    user_id: Optional[str],
    page: int,
    limit: int,
    since: Optional[datetime],
):
    query = db.query(Story)

    # Si se manda usuario, filtra por usuario.
    # Si NO se manda usuario, muestra TODAS las historias.
    if user_id:
        query = query.filter(Story.user_id == user_id)

    if since:
        query = query.filter(Story.updated_at > since)

    total = query.count()

    items = (
        query.order_by(Story.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if total else 1,
    }


def get_story_by_id(db: Session, story_id: int) -> Story:
    return _get_or_404(db, story_id)


def create_story(db: Session, payload: StoryCreate, user_id: str) -> Story:
    story = Story(
        title=payload.title,
        section=payload.section,
        body=payload.body,
        image_url=str(payload.image_url),
        user_id=user_id,
    )

    db.add(story)
    db.commit()
    db.refresh(story)

    return story


def update_story(
    db: Session,
    story_id: int,
    payload: StoryUpdate,
    user_id: str,
) -> Story:
    story = _get_or_404(db, story_id)
    _assert_owner(story, user_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "image_url" and value is not None:
            value = str(value)

        setattr(story, field, value)

    story.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(story)

    return story


def replace_story(
    db: Session,
    story_id: int,
    payload: StoryCreate,
    user_id: str,
) -> Story:
    story = _get_or_404(db, story_id)
    _assert_owner(story, user_id)

    story.title = payload.title
    story.section = payload.section
    story.body = payload.body
    story.image_url = str(payload.image_url)
    story.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(story)

    return story


def delete_story(db: Session, story_id: int, user_id: str):
    story = _get_or_404(db, story_id)
    _assert_owner(story, user_id)

    db.delete(story)
    db.commit()
