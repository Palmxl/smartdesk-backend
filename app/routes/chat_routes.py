from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from app.services.websocket_manager import (
    manager
)

router = APIRouter()

@router.websocket("/chat")
async def chat_socket(
    websocket: WebSocket
):

    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            await manager.broadcast(data)

    except WebSocketDisconnect:

        manager.disconnect(websocket)