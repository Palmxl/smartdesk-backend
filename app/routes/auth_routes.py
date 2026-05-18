from fastapi import APIRouter

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.database.connection import (
    SessionLocal
)

from app.models.user_model import User

from app.schemas.user_schema import (
    UserCreate,
    UserLogin
)

from app.services.auth_service import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/register")
def register(user: UserCreate):

    db: Session = SessionLocal()

    try:

        hashed_password = (
            pwd_context.hash(
                user.password
            )
        )

        new_user = User(
            username=user.username,
            password=hashed_password,
            role=user.role
        )

        db.add(new_user)

        db.commit()

        return {
            "message": "User created"
        }

    finally:

        db.close()

@router.post("/login")
def login(user: UserLogin):

    db: Session = SessionLocal()

    try:

        db_user = (
            db.query(User)
            .filter(
                User.username
                == user.username
            )
            .first()
        )

        if not db_user:

            return {
                "error":
                    "Invalid credentials"
            }

        valid_password = (
            pwd_context.verify(
                user.password,
                db_user.password
            )
        )

        if not valid_password:

            return {
                "error":
                    "Invalid credentials"
            }

        token = create_access_token({
            "sub": db_user.username,
            "role": db_user.role
        })

        return {
            "access_token": token
        }

    finally:

        db.close()