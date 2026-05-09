from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from datetime import datetime

from app.database.base import Base

class TicketComment(Base):

    __tablename__ = "ticket_comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    username = Column(
        String,
        nullable=False
    )

    content = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )