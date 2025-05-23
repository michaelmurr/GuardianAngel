from app.websocket.errors import UnknownMessageFormat, WebSocketError
from app.websocket.messages import WebsocketMessageType, WebsocketStatusMessage
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)

    async def send_json_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

    def is_type_in_dict(self, message: dict) -> bool:
        return "type" in message and isinstance(message["type"], str)

    async def handle_message(self, message: dict, user_id: str):
        if not self.is_type_in_dict(message):
            raise UnknownMessageFormat(
                "message could not be identified since type property is missing"
            )
        message_type = message["type"]

        match message_type:
            case WebsocketMessageType.STATUS:
                parsed_message = WebsocketStatusMessage.model_construct(**message)
            case _:
                raise UnknownMessageFormat(
                    f"message type {message_type} is not supported"
                )

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def handle_connection(self, ws: WebSocket, user_id: str):
        try:
            await self.connect(user_id, ws)
            while True:
                try:
                    data = await ws.receive_json()
                    try:
                        await self.handle_message(data, user_id)
                    except WebSocketError as e:
                        await ws.send_json(e.to_message())
                        print(f"Websocket error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")

                    print(f"Received data from {user_id}: {data}")
                except Exception as e:
                    print(f"Error receiving data from {user_id}: {e}")
                    break
        except Exception as e:
            print(f"Connection error for {user_id}: {e}")
        finally:
            self.disconnect(user_id)


CONNECTION_MANAGER = ConnectionManager()


def get_connection_manager():
    return CONNECTION_MANAGER
