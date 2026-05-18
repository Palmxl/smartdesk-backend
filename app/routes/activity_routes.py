from fastapi import APIRouter

from sqlalchemy.orm import Session

from app.database.connection import (
    SessionLocal
)

from app.models.activity_log_model import (
    ActivityLog
)

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)

@router.get("/")
def get_activities():

    db: Session = SessionLocal()

    try:

        logs = (
            db.query(ActivityLog)
            .order_by(
                ActivityLog.created_at.desc()
            )
            .all()
        )

        return logs

    finally:

        db.close()