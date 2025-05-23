from enum import Enum

from pydantic import BaseModel

from app.types.general import Location


class TrackingTaskAction(str, Enum):
    START = "START"
    STOP = "STOP"



class TrackingTaskMessage(BaseModel):
    """Class for managing user's walk"""

    uid: str
    action: TrackingTaskAction
    destination: Location | None