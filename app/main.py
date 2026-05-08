from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base

from app.routes.ticket_routes import router as ticket_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ticket_router)

@app.get("/")
def root():
    return {"message": "SmartDesk API"}