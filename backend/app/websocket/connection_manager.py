from app.pubsub.live_data import publish_live_user_data
from app.websocket.errors import UnknownMessageFormat, WebSocketError
from app.websocket.messages import WebsocketMessageType, WebsocketStatusMessage
from app.websocket.websocket_connection import WebSocketConnection, WebSocketMetaData
from fastapi import WebSocket

USERID = str


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[USERID, WebSocketConnection] = {}

    async def connect(self, websocket: WebSocket, metadata: WebSocketMetaData):
        await websocket.accept()
        self.active_connections[metadata.user_id] = WebSocketConnection(
            websocket=websocket, metadata=metadata
        )

    def disconnect(self, user_id: USERID):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: USERID):
        if user_id in self.active_connections:
            connection = self.active_connections[user_id]
            await connection.websocket.send_text(message)

    async def send_json_message(self, message: dict, user_id: USERID):
        if user_id in self.active_connections:
            connection = self.active_connections[user_id]
            await connection.websocket.send_json(message)

    def is_type_in_dict(self, message: dict) -> bool:
        return "type" in message and isinstance(message["type"], str)

    async def handle_message(self, message: dict, metadata: WebSocketMetaData):
        if not self.is_type_in_dict(message):
            raise UnknownMessageFormat(
                "message could not be identified since type property is missing"
            )
        message_type = message["type"]

        match message_type:
            case WebsocketMessageType.STATUS:
                parsed_message = WebsocketStatusMessage(**message)
                publish_live_user_data(
                    metadata.user_id, metadata.device_id, parsed_message.payload
                )
            case _:
                raise UnknownMessageFormat(
                    f"message type {message_type} is not supported"
                )

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def handle_connection(self, ws: WebSocket, metadata: WebSocketMetaData):
        try:
            await self.connect(ws, metadata)
            while True:
                try:
                    data = await ws.receive_json()
                    try:
                        await self.handle_message(data, metadata)
                    except WebSocketError as e:
                        await ws.send_json(e.to_message())
                        print(f"Websocket error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")

                    print(f"Received data from {metadata.user_id}: {data}")
                except Exception as e:
                    print(f"Error receiving data from {metadata.user_id}: {e}")
                    break
        except Exception as e:
            print(f"Connection error for {metadata.user_id}: {e}")
        finally:
            self.disconnect(metadata.user_id)


CONNECTION_MANAGER = ConnectionManager()


def get_connection_manager():
    return CONNECTION_MANAGER
