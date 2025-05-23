from ctypes import Union
from enum import Enum

from app.types.general import UserRealtimeData
from pydantic import BaseModel


class WebsocketMessageType(str, Enum):
    STATUS = "status"


class WebsocketStatusMessage(BaseModel):
    type: str = "status"
    payload: UserRealtimeData


WebsocketMessage = WebsocketStatusMessage
