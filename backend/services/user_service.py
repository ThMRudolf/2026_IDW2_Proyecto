"""
Service layer for user account management.

Handles creation and lookup of User records. UUID generation is done
here so the client only needs to persist the opaque x_user_id token.
"""

import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate


def create_user(db: Session, payload: UserCreate) -> User:
    """
    Create a new user account and persist it to the database.

    Objective:
        Instantiate a User record from the validated payload, assign a
        fresh UUID as the x_user_id token, and commit it to the database.

    Inputs:
        db      (Session)    -- Active SQLAlchemy database session.
        payload (UserCreate) -- Validated data containing username and email.

    Output (User):
        The newly created and refreshed User ORM instance, including the
        generated x_user_id that the client must store for future requests.
    """
    user = User(
        username=payload.username,
        email=payload.email,
        x_user_id=str(uuid.uuid4()),   # generate UUID here, client stores it
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_x_id(db: Session, x_user_id: str) -> User:
    """
    Retrieve a user by their opaque UUID token.

    Objective:
        Look up a User record using the x_user_id that was issued at
        registration time and raise a 404 if it does not exist.

    Inputs:
        db         (Session) -- Active SQLAlchemy database session.
        x_user_id  (str)     -- UUID token issued to the client at signup.

    Output (User):
        The matching User ORM instance.

    Raises:
        HTTPException 404 -- If no user with the given x_user_id exists.
    """
    user = db.query(User).filter(User.x_user_id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
