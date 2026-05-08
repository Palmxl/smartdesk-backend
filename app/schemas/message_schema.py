from pydantic import BaseModel

class MessageResponse(BaseModel):

    id: int

    username: str

    content: str

    class Config:
        from_attributes = True