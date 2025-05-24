from typing import List, Union

from app.types.general import Location
from pydantic import BaseModel


class EmergencyNearbyPayload(BaseModel):
    user_id: str
    location: Location


class OutboundNearbyEmergencyMessage(BaseModel):
    type: str = "emergency_nearby"
    payload: EmergencyNearbyPayload


class RouteCompletedPayload(BaseModel):
    user_id: str


class OutboundCompletedRouteMessage(BaseModel):
    type: str = "route_completed"
    payload: RouteCompletedPayload


class FriendEmergencyPayload(BaseModel):
    user_id: str
    location: Location


class OutboundFriendEmergencyMessage(BaseModel):
    type: str = "friend_emergency"
    payload: EmergencyNearbyPayload


class FriendLocationUpdatePayload(BaseModel):
    user_id: str
    location: Location


class OutboundFriendLocationUpdateMessage(BaseModel):
    type: str = "friend_location_update"
    payload: List[FriendLocationUpdatePayload]


OutboundMessage = Union[
    OutboundNearbyEmergencyMessage,
    OutboundFriendEmergencyMessage,
    OutboundCompletedRouteMessage,
    OutboundFriendLocationUpdateMessage,
]


# TODO friend emergency, emergency nearby, emergency triggerd
# all messages have a type field that identify them
# plus a payload think about the payloads
