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

    class Config:
        from_attributes = True