from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return user_id