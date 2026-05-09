from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.database.connection import (
    Base
)
class Message(Base):

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )