import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate


def create_user(db: Session, payload: UserCreate) -> User:
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
    user = db.query(User).filter(User.x_user_id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
