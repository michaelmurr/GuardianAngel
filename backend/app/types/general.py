from pydantic import BaseModel


class Location(BaseModel):
    longitude: float
    latitude: float


class UserRealtimeData(BaseModel):
    """Class for tracking updates of the user."""

    location: Location
    battery: float
    speed: float
