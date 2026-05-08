from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):

        self.active_connections = []

        self.online_users = set()

    async def connect(
        self,
        websocket: WebSocket,
        username: str
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

        self.online_users.add(username)

        await self.broadcast_online_users()

    def disconnect(
        self,
        websocket: WebSocket,
        username: str
    ):

        self.active_connections.remove(
            websocket
        )

        self.online_users.discard(
            username
        )

    async def broadcast(
        self,
        message: str
    ):

        for connection in (
            self.active_connections
        ):

            await connection.send_text(
                message
            )

    async def broadcast_online_users(
        self
    ):

        message = (
            f"ONLINE_USERS:"
            f"{len(self.online_users)}"
        )

        await self.broadcast(message)

manager = ConnectionManager()