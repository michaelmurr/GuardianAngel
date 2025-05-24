import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TrackingTaskAction(str, Enum):
    START = "START"
    STOP = "STOP"


class TrackingTaskMessage(BaseModel):
    """Class for managing user's walk"""

    uid: str
    device_id: str
    action: TrackingTaskAction
    polyline: Optional[str] = None
    time_needed: Optional[datetime.timedelta] = None
