from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from sqlalchemy.orm import Session

from app.database.connection import (
    SessionLocal
)

from app.models.message_model import (
    Message
)

from app.services.websocket_manager import (
    manager
)

router = APIRouter()

@router.websocket("/chat/{username}")
async def chat_socket(
    websocket: WebSocket,
    username: str
):

    await manager.connect(
        websocket,
        username
    )

    db: Session = SessionLocal()

    try:

        while True:

            try:

                data = (
                    await websocket
                    .receive_text()
                )

            except:

                break

            parts = data.split(
                ":",
                1
            )

            if len(parts) < 2:
                continue

            username = (
                parts[0]
                .strip()
            )

            content = (
                parts[1]
                .strip()
            )

            new_message = Message(
                username=username,
                content=content
            )

            db.add(new_message)

            db.commit()

            db.refresh(new_message)

            await manager.broadcast(
                data
            )

    finally:

        manager.disconnect(
            websocket,
            username
        )

        await manager.broadcast_online_users()

        db.close()


@router.get("/messages")
def get_messages():

    db: Session = SessionLocal()

    try:

        messages = (
            db.query(Message)
            .all()
        )

        return messages

    finally:

        db.close()