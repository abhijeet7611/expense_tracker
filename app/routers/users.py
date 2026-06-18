from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app import (
    models,
    schemas,
    utils,
    auth
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=schemas.UserResponse
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = utils.hash_password(
        user.password
    )

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not utils.verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = auth.create_access_token(
    data={
        "user_id": db_user.id,
        "email": db_user.email
    }
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }