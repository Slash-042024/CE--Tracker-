from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import hash_password

router = APIRouter(prefix='/users', tags=['users'])

@router.get("/me", response_model=UserResponse)

def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)


def update_me(user_update: UserUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user = current_user
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        user.email = user_update.email
    if user_update.password is not None:
        user.password_hash = hash_password(user_update.password)

    db.commit()
    db.refresh(user)
    return user

