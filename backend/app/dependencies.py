from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    user_id: int | None = Cookie(None),
    db: Session = Depends(get_db)) -> User:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def get_optional_user(
    user_id: int | None = Cookie(None),
    db: Session = Depends(get_db)
) -> User | None:
    """Get the current user if authenticated, otherwise None."""
    if user_id is None:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user
