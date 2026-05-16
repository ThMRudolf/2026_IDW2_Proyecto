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
    return user_service.create_user(db, payload)


@router.get("/me", response_model=UserRead)
def get_me(
    x_user_id: str = Header(...),
    db: Session = Depends(get_db),
):
    return user_service.get_user_by_x_id(db, x_user_id)
