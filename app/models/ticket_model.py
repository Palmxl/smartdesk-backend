from sqlalchemy import Column, Integer, String, Text

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