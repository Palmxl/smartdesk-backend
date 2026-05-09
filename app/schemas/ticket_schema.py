import datetime

from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    description: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    sentiment: str
    category: str
    assigned_to: str | None
    summary: str | None
    created_at: datetime
    sla_deadline: datetime | None

    class Config:
        from_attributes = True