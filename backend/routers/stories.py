"""
Router for user-generated story endpoints.

Full CRUD access to stories scoped to the authenticated user via the
X-User-Id request header. Supports pagination and optional date filtering
on the listing endpoint.
All routes are prefixed with /api/stories.
"""

from fastapi import APIRouter, Depends, Header, HTTPException
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
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of stories visible to the authenticated user.

    Objective:
        Return stories in reverse-chronological order, optionally restricted
        to those created after a given timestamp.

    Inputs (query params):
        page  (int, default=1)               -- 1-based page number to retrieve.
        limit (int, default=10)              -- Maximum number of stories per page.
        since (datetime, optional)           -- ISO-8601 timestamp; when provided
                                               only stories created after this
                                               moment are returned.

    Inputs (headers):
        X-User-Id (str, required) -- Identifier of the authenticated user.

    Output (PaginatedResponse[StoryRead]):
        items (List[StoryRead]) -- Stories on the requested page. Each entry contains:
            id         (int)      -- Unique story identifier.
            title      (str)      -- Story headline.
            section    (str)      -- Section or category the story belongs to.
            body       (str)      -- Full story text.
            image_url  (str)      -- URL of the story cover image.
            user_id    (str)      -- X-User-Id of the story author.
            created_at (datetime) -- Creation timestamp (UTC).
            updated_at (datetime) -- Last update timestamp (UTC).
        total (int) -- Total number of stories matching the filter.
        page  (int) -- Current page number.
        limit (int) -- Page size used for this response.
        pages (int) -- Total number of available pages.
    """
    return story_service.get_stories(db, x_user_id, page, limit, since)


@router.get("/{story_id}", response_model=StoryRead)
def get_story(
    story_id: int,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Retrieve a single story by its ID.

    Objective:
        Return the full details of one story identified by its primary key.

    Inputs (path param):
        story_id (int) -- Primary key of the story to retrieve.

    Inputs (headers):
        X-User-Id (str, required) -- Identifier of the authenticated user.

    Output (StoryRead):
        id         (int)      -- Unique story identifier.
        title      (str)      -- Story headline.
        section    (str)      -- Section or category the story belongs to.
        body       (str)      -- Full story text.
        image_url  (str)      -- URL of the story cover image.
        user_id    (str)      -- X-User-Id of the story author.
        created_at (datetime) -- Creation timestamp (UTC).
        updated_at (datetime) -- Last update timestamp (UTC).

    Raises:
        404 Not Found -- If no story with the given ID exists.
    """
    return story_service.get_story_by_id(db, story_id)


@router.post("", response_model=StoryRead, status_code=201)
def create_story(
    payload: StoryCreate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Create a new story attributed to the authenticated user.

    Objective:
        Persist a new story record and return the created object with its
        server-assigned ID and timestamps.

    Inputs (body — StoryCreate):
        title     (str)     -- Story headline.
        section   (str)     -- Section or category the story belongs to.
        body      (str)     -- Full story text.
        image_url (HttpUrl) -- URL of the story cover image.

    Inputs (headers):
        X-User-Id (str, required) -- Identifier of the authenticated user;
                                     stored as the story's author.

    Output (StoryRead, HTTP 201):
        id         (int)      -- Unique story identifier assigned by the database.
        title      (str)      -- Story headline.
        section    (str)      -- Section or category the story belongs to.
        body       (str)      -- Full story text.
        image_url  (str)      -- URL of the story cover image.
        user_id    (str)      -- X-User-Id of the story author.
        created_at (datetime) -- Creation timestamp (UTC).
        updated_at (datetime) -- Last update timestamp (UTC).
    """
    return story_service.create_story(db, payload, x_user_id)


@router.patch("/{story_id}", response_model=StoryRead)
def patch_story(
    story_id: int,
    payload: StoryUpdate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Partially update an existing story.

    Objective:
        Apply a partial update to a story. Only the fields present in the
        request body are modified; omitted fields keep their current values.

    Inputs (path param):
        story_id (int) -- Primary key of the story to update.

    Inputs (body — StoryUpdate, all fields optional):
        title     (str, optional)     -- New story headline.
        section   (str, optional)     -- New section or category.
        body      (str, optional)     -- New full story text.
        image_url (HttpUrl, optional) -- New URL of the story cover image.

    Inputs (headers):
        X-User-Id (str, required) -- Must match the story's original author.

    Output (StoryRead):
        The story object with all fields reflecting the applied changes.

    Raises:
        403 Forbidden -- If X-User-Id does not match the story's author.
        404 Not Found -- If no story with the given ID exists.
    """
    return story_service.update_story(db, story_id, payload, x_user_id)


@router.put("/{story_id}", response_model=StoryRead)
def replace_story(
    story_id: int,
    payload: StoryCreate,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Fully replace an existing story.

    Objective:
        Overwrite all editable fields of a story with the values provided in
        the request body. All fields are required (unlike PATCH).

    Inputs (path param):
        story_id (int) -- Primary key of the story to replace.

    Inputs (body — StoryCreate):
        title     (str)     -- New story headline.
        section   (str)     -- New section or category.
        body      (str)     -- New full story text.
        image_url (HttpUrl) -- New URL of the story cover image.

    Inputs (headers):
        X-User-Id (str, required) -- Must match the story's original author.

    Output (StoryRead):
        The story object with all fields reflecting the replacement values.

    Raises:
        403 Forbidden -- If X-User-Id does not match the story's author.
        404 Not Found -- If no story with the given ID exists.
    """
    return story_service.replace_story(db, story_id, payload, x_user_id)


@router.delete("/{story_id}", status_code=204)
def delete_story(
    story_id: int,
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Delete a story.

    Objective:
        Permanently remove a story from the database.

    Inputs (path param):
        story_id (int) -- Primary key of the story to delete.

    Inputs (headers):
        X-User-Id (str, required) -- Must match the story's original author.

    Output:
        HTTP 204 No Content -- Empty body on success.

    Raises:
        403 Forbidden -- If X-User-Id does not match the story's author.
        404 Not Found -- If no story with the given ID exists.
    """
    story_service.delete_story(db, story_id, x_user_id)
