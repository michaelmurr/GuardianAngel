from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel

class Action(str, Enum):
    START = 'START'
    STOP = 'STOP'


class Location(BaseModel):
    longitude: float
    latitude: float


class UserRealtimeData(BaseModel):
    """Class for tracking updates of the user."""
    location: Location
    battery: float
    speed: float


class UserWalkControlData(BaseModel):
    """Class for managing user's walk"""
    uid: str
    action: Action
    destination: Location | None
    
