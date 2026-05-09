from fastapi import (
    FastAPI,
    WebSocket
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.database.connection import (
    engine,
    Base
)

from app.models.user_model import (
    User
)

from app.models.ticket_model import (
    Ticket
)

from app.models.activity_log_model import (
    ActivityLog
)

from app.routes.ticket_routes import (
    router as ticket_router
)

from app.routes.auth_routes import (
    router as auth_router
)

from app.routes.chat_routes import (
    router as chat_router
)

from app.routes.activity_routes import (
    router as activity_router
)

from app.websockets.ticket_ws import (
    connect_ticket_ws,
    disconnect_ticket_ws
)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    ticket_router
)

app.include_router(
    auth_router
)

app.include_router(
    chat_router
)

app.include_router(
    activity_router
)

@app.get("/")
def root():

    return {
        "message":
            "SmartDesk API"
    }

@app.websocket("/tickets/ws")
async def ticket_ws(
    websocket: WebSocket
):

    await connect_ticket_ws(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except:

        await disconnect_ticket_ws(
            websocket
        )