from dataclasses import dataclass

from fastapi import WebSocket


@dataclass
class WebSocketMetaData:
    user_id: str
    device_id: str


@dataclass
class WebSocketConnection:
    websocket: WebSocket
    metadata: WebSocketMetaData
