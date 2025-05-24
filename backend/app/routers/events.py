from typing import Annotated

from dependencies import db_dependency, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request, status
from settings import env

from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship
from app.pubsub.tracking_task import publish_tracking_task
from app.schemas.events import EmergencyUserDataDTO
from app.services.user_location_service import get_user_location_service
from app.types.general import EmergencyUserData
from app.types.tracking import TrackingTaskAction, TrackingTaskMessage
from app.utils import delete_users_route
from app.websocket.connection_manager import ConnectionManager, get_connection_manager
from app.websocket.outbound_messages import (
    EmergencyNearbyPayload,
    OutboundNearbyEmergencyMessage,
)


def validate_track_header(request: Request):
    header_value = request.headers.get("X-TRACK-API")
    if not header_value or header_value != env.TRACKING_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TRACK-API header",
        )
    return header_value


router = APIRouter()


@router.post("/emergency/tracking")
async def tracking_emergency(
    db: db_dependency,
    # TODO uncomment for prod : token: Annotated[str, Depends(validate_track_header)],
    con_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    emergency_data: EmergencyUserData,
):
    # deleting route from db
    try:
        await delete_users_route(emergency_data.uid, db)
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete route",
        )

    # sending the message to the user
    con_manager.send_message(emergency_data.uid, emergency_data.reason)

    # sending message to all connected users
    user_location_service = get_user_location_service()
    user_list = (
        user_location_service.get_uids_for_nearby_user_devices_by_uid_and_device(
            emergency_data.uid, emergency_data.device_id
        )
    )
    user_location = user_location_service.get_location_by_uid_and_device(
        emergency_data.uid, emergency_data.device_id
    )
    message = OutboundNearbyEmergencyMessage(
        payload=EmergencyNearbyPayload(
            user_id=emergency_data.uid, location=user_location
        )
    )

    con_manager.broadcast_message(user_list, message)

    # sending message to all friends
    friends = (
        db.query(UserDB)
        .join(friendship, UserDB.username == friendship.c.friend_id)
        .filter(friendship.c.user_id == emergency_data.uid)
        .all()
    )

    friends = [friend.username for friend in friends]

    con_manager.broadcast_message(friends, message)

    return emergency_data  # TODO : return emergency message


@router.post("/completed")
async def tracking_completed(
    db: db_dependency, token: Annotated[str, Depends(validate_track_header)]
):
    # deleting route from db
    # try:
    #     await delete_users_route(emer.uid, db)
    # except Exception as e:
    #     db.rollback()
    #     print(f"Database error: {str(e)}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Failed to delete route",
    #     )

    return {"validated": True}


@router.post("/emergency/ui")
async def ui_emergency(
    db: db_dependency,
    current_user: Annotated[str, Depends(get_current_user)],
    con_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    emergency_data: EmergencyUserDataDTO,
):
    print(f"user_id: {emergency_data.uid}")
    try:
        await delete_users_route(emergency_data.uid, db)
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete route",
        )

    publish_tracking_task(
        TrackingTaskMessage(
            uid=emergency_data.uid,
            device_id=emergency_data.device_id,
            action=TrackingTaskAction.STOP,
        )
    )

    user_location_service = get_user_location_service()
    user_list = (
        user_location_service.get_uids_for_nearby_user_devices_by_uid_and_device(
            emergency_data.uid, emergency_data.device_id
        )
    )
    print(f"Users nearby: {user_list}")
    user_location = user_location_service.get_location_by_uid_and_device(
        emergency_data.uid, emergency_data.device_id
    )
    print("User Location:", user_location)
    message = OutboundNearbyEmergencyMessage(
        payload=EmergencyNearbyPayload(
            user_id=emergency_data.uid, location=user_location
        )
    )

    await con_manager.broadcast_message(user_list, message)
