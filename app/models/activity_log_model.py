from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime

from app.database.connection import Base

class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action = Column(String)

    username = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )