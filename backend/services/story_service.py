"""
Service layer for user-authored stories (fan content).

Handles full CRUD lifecycle for Story records. All write operations
enforce ownership: only the story's author (matched by x_user_id) may
modify or delete it.
"""

import math
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Story
from schemas import StoryCreate, StoryUpdate


def _assert_owner(story: Story, user_id: str):
    """
    Guard: raise 403 if user_id does not match the story's author.

    Inputs:
        story   (Story) -- The Story ORM instance being checked.
        user_id (str)   -- x_user_id of the requesting user.

    Raises:
        HTTPException 403 -- If the requesting user does not own the story.
    """
    if story.user_id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission to modify this story")


def _get_or_404(db: Session, story_id: int) -> Story:
    """
    Fetch a Story by ID or raise 404 if it does not exist.

    Inputs:
        db       (Session) -- Active SQLAlchemy database session.
        story_id (int)     -- Primary key of the story to fetch.

    Output (Story):
        The matching Story ORM instance.

    Raises:
        HTTPException 404 -- If no story with the given ID exists.
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


def get_stories(
    db: Session,
    user_id: str,
    page: int,
    limit: int,
    since: Optional[datetime],
):
    """
    Retrieve a paginated list of stories for a specific user.

    Objective:
        Return all Story rows that belong to user_id, optionally limited
        to those updated after a given timestamp. Results are ordered
        from newest to oldest by creation date.

    Inputs:
        db      (Session)           -- Active SQLAlchemy database session.
        user_id (str)               -- x_user_id of the story author.
        page    (int)               -- 1-based page number.
        limit   (int)               -- Maximum number of records per page.
        since   (Optional[datetime])-- If provided, only stories with
                                       updated_at > since are returned.

    Output (dict):
        items (List[Story]) -- Stories on the requested page.
        total (int)         -- Total number of matching stories.
        page  (int)         -- Current page number.
        limit (int)         -- Page size used for this response.
        pages (int)         -- Total number of available pages.
    """
    query = db.query(Story).filter(Story.user_id == user_id)

    if since:
        query = query.filter(Story.updated_at > since)

    total = query.count()
    items = (
        query
        .order_by(Story.created_at.desc())
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
    """
    Retrieve a single story by its primary key.

    Objective:
        Public wrapper around _get_or_404 for router use.

    Inputs:
        db       (Session) -- Active SQLAlchemy database session.
        story_id (int)     -- Primary key of the story to retrieve.

    Output (Story):
        The matching Story ORM instance.

    Raises:
        HTTPException 404 -- If no story with the given ID exists.
    """
    return _get_or_404(db, story_id)


def create_story(db: Session, payload: StoryCreate, user_id: str) -> Story:
    """
    Create a new story and persist it to the database.

    Objective:
        Instantiate a Story record from the validated payload, associate
        it with the requesting user, and commit it to the database.

    Inputs:
        db      (Session)     -- Active SQLAlchemy database session.
        payload (StoryCreate) -- Validated story data (title, section, body, image_url).
        user_id (str)         -- x_user_id of the story author.

    Output (Story):
        The newly created and refreshed Story ORM instance.
    """
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


def update_story(db: Session, story_id: int, payload: StoryUpdate, user_id: str) -> Story:
    """
    Partially update a story (PATCH semantics).

    Objective:
        Apply only the supplied fields from payload to the existing story,
        refresh updated_at, and commit. Ownership is verified before any
        change is applied.

    Inputs:
        db       (Session)     -- Active SQLAlchemy database session.
        story_id (int)         -- Primary key of the story to update.
        payload  (StoryUpdate) -- Partial data; only set fields are applied.
        user_id  (str)         -- x_user_id of the requesting user.

    Output (Story):
        The updated and refreshed Story ORM instance.

    Raises:
        HTTPException 404 -- If no story with the given ID exists.
        HTTPException 403 -- If the requesting user does not own the story.
    """
    story = _get_or_404(db, story_id)
    _assert_owner(story, user_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(story, field, value)

    story.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(story)
    return story


def replace_story(db: Session, story_id: int, payload: StoryCreate, user_id: str) -> Story:
    """
    Fully replace a story's content (PUT semantics).

    Objective:
        Overwrite all mutable fields (title, section, body, image_url) of
        an existing story with the complete payload and commit. Ownership
        is verified before any change is applied.

    Inputs:
        db       (Session)     -- Active SQLAlchemy database session.
        story_id (int)         -- Primary key of the story to replace.
        payload  (StoryCreate) -- Complete new data for the story.
        user_id  (str)         -- x_user_id of the requesting user.

    Output (Story):
        The replaced and refreshed Story ORM instance.

    Raises:
        HTTPException 404 -- If no story with the given ID exists.
        HTTPException 403 -- If the requesting user does not own the story.
    """
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
    """
    Delete a story from the database.

    Objective:
        Remove an existing story after verifying the requesting user owns it.

    Inputs:
        db       (Session) -- Active SQLAlchemy database session.
        story_id (int)     -- Primary key of the story to delete.
        user_id  (str)     -- x_user_id of the requesting user.

    Output:
        None. The story is deleted and the transaction is committed.

    Raises:
        HTTPException 404 -- If no story with the given ID exists.
        HTTPException 403 -- If the requesting user does not own the story.
    """
    story = _get_or_404(db, story_id)
    _assert_owner(story, user_id)

    db.delete(story)
    db.commit()
