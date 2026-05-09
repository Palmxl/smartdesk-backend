from fastapi import WebSocket

ticket_connections = []

async def connect_ticket_ws(
    websocket: WebSocket
):

    await websocket.accept()

    ticket_connections.append(
        websocket
    )

async def disconnect_ticket_ws(
    websocket: WebSocket
):

    ticket_connections.remove(
        websocket
    )

async def broadcast_ticket(
    message: str
):

    for connection in ticket_connections:

        await connection.send_text(
            message
        )