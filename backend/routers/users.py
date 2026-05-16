"""
Router for user account endpoints.

Handles user registration and profile retrieval. Authentication is performed
via the X-User-Id header that the frontend stores in sessionStorage after
login.
All routes are prefixed with /api/users.
"""

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserRead
from services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.

    Objective:
        Persist a new user record and return the created profile. The server
        generates the x_user_id value that the frontend must store and send
        in subsequent requests via the X-User-Id header.

    Inputs (body — UserCreate):
        username (str) -- Desired display name for the user.
        email    (str) -- User's email address (must be unique).

    Output (UserRead, HTTP 201):
        id         (int)      -- Unique user identifier.
        username   (str)      -- Display name.
        email      (str)      -- Email address.
        x_user_id  (str)      -- Server-generated token used as the auth header
                                 in all authenticated requests.
        created_at (datetime) -- Account creation timestamp (UTC).

    Raises:
        409 Conflict -- If the email is already registered.
    """
    return user_service.create_user(db, payload)


@router.get("/me", response_model=UserRead)
def get_me(
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Retrieve the profile of the currently authenticated user.

    Objective:
        Look up and return the user whose x_user_id matches the value sent
        in the X-User-Id header. Used by the frontend to rehydrate the session
        on page load.

    Inputs (headers):
        X-User-Id (str, required) -- Token obtained during registration; acts
                                     as the session identifier.

    Output (UserRead):
        id         (int)      -- Unique user identifier.
        username   (str)      -- Display name.
        email      (str)      -- Email address.
        x_user_id  (str)      -- The same token sent in the header.
        created_at (datetime) -- Account creation timestamp (UTC).

    Raises:
        404 Not Found -- If no user with the given X-User-Id exists.
    """
    return user_service.get_user_by_x_id(db, x_user_id)
