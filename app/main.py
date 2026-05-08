from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.base import Base

from app.routes.ticket_routes import router as ticket_router

from app.routes.auth_routes import (
    router as auth_router
)

from app.routes.websocket_routes import (
    router as websocket_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "SmartDesk API"}