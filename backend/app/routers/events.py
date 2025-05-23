from typing import Annotated

from app.websocket.connection_manager import ConnectionManager, get_connection_manager
from app.utils import delete_users_route
from dependencies import db_dependency, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request, status
from settings import env
from pydantic import BaseModel
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship


def validate_track_header(request: Request):
    header_value = request.headers.get("X-TRACK-API")
    if not header_value or header_value != env.TRACKING_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TRACK-API header",
        )
    return header_value

class EmergencyUserData(BaseModel):
    uid: str
    device_id: str 
    reason: str

router = APIRouter()

@router.post('/emergency/tracking')
async def emergency_event(db: db_dependency, 
                          # TODO uncomment for prod : token: Annotated[str, Depends(validate_track_header)], 
                          con_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
                          emergency_data: EmergencyUserData):
    
    # deleting route from db
    try:
        await delete_users_route(emergency_data.uid, db);
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete route")

    #sending the message to the user
    con_manager.send_json_message(emergency_data.uid, emergency_data.reason)


    # sending message to all connected users
    for ws in con_manager.broadcast_json_message(): 
        pass

    # sending message to all friends
    friends = (
        db.query(UserDB)
        .join(friendship, UserDB.username == friendship.c.friend_id)
        .filter(friendship.c.user_id == emergency_data.uid)
        .all()
    )

    for friend in friends:
        con_manager.send_json_message(friend.username, emergency_data.reason)
    
    return emergency_data #TODO : return emergency message
    


@router.post('/completed/tracking')
async def emergency_event(db: db_dependency, token: Annotated[str, Depends(validate_track_header)]):
    return {"validated": True}


@router.post('/emergency/ui')
async def emergency_event(db: db_dependency, current_user: Annotated[str, Depends(get_current_user)]):
   return {"validated": True}


@router.post('/completed/ui')
async def emergency_event(db: db_dependency, current_user: Annotated[str, Depends(get_current_user)]):
   return {"validated": True}



