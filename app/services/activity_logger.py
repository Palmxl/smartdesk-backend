from sqlalchemy.orm import Session

from app.models.activity_log_model import (
    ActivityLog
)

def log_activity(
    db: Session,
    action: str,
    username: str
):

    log = ActivityLog(
        action=action,
        username=username
    )

    db.add(log)

    db.commit()