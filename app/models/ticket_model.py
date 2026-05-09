from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import DateTime
from datetime import datetime

from app.database.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    priority = Column(String, default="Low")

    status = Column(String, default="Open")

    sentiment = Column(String, default="Neutral")

    category = Column(String, default="General")

    assigned_to = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    sla_deadline = Column(DateTime, nullable=True)

    summary = Column(Text, nullable=True)

    ai_response = Column(Text, nullable=True)