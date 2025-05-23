from enum import Enum

from app.types.general import Location
from pydantic import BaseModel


class TrackingTaskAction(str, Enum):
    START = "START"
    STOP = "STOP"


class TrackingTaskMessage(BaseModel):
    """Class for managing user's walk"""

    uid: str
    device_id: str
    action: TrackingTaskAction
    destination: Location | None
