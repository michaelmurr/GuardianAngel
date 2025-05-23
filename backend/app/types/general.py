from pydantic import BaseModel, Field


class Location(BaseModel):
    longitude: float
    latitude: float


class UserRealtimeData(BaseModel):
    """Class for tracking updates of the user."""

    location: Location
    battery: float = Field(..., ge=0.0, le=100.0)
    speed: float = Field(..., ge=0.0)


class EmergencyUserData(BaseModel):
    uid: str
    device_id: str
    reason: str
