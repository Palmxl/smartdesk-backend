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

        self.online_users.add(
            username
        )

        await self.broadcast_online_users()

    def disconnect(
        self,
        websocket: WebSocket,
        username: str
    ):

        if websocket in (
            self.active_connections
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

        disconnected = []

        for connection in (
            self.active_connections
        ):

            try:

                await connection.send_text(
                    message
                )

            except:

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            if connection in (
                self.active_connections
            ):

                self.active_connections.remove(
                    connection
                )

    async def broadcast_online_users(
        self
    ):

        message = (
            f"ONLINE_USERS:"
            f"{len(self.online_users)}"
        )

        await self.broadcast(
            message
        )

manager = ConnectionManager()