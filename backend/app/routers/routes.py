
from datetime import datetime
import logging
from typing import Annotated, Any
from app.models.pyd.user import  FriendAddRequest, RouteCreateRequest, UpdateUserModel
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.google_maps import get_google_maps_client
from app.models.alchemy.route import Route as RouteDB
from app.models.pyd.route import Route as RoutePyd
from app.pubsub.tracking_task import publish_tracking_task
from app.types.tracking import TrackingTaskAction, TrackingTaskMessage
from app.utils import delete_users_route
from dependencies import get_current_user
from dependencies import db_dependency


router = APIRouter()



@router.post('/create')
async def get_current_route(current_user: Annotated[UserPyd, Depends(get_current_user)], 
                            db: db_dependency, 
                            gmaps: Annotated[Any , Depends(get_google_maps_client)], 
                            request: RouteCreateRequest):
   
    try:
        current_route = db.query(RouteDB).filter(RouteDB.user_id == current_user.username).first()
        if current_route:
            route_pyd = RoutePyd(
                start_ll=current_route.start_ll,
                end_ll=current_route.end_ll,
                duration=current_route.duration,
                distance=current_route.distance,
                polyline=current_route.polyline,
                start_address=current_route.start_address,
                end_address=current_route.end_address
                )
            return route_pyd
        
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    
    now = datetime.now()
    start = request.start_ll
    end = request.end_ll
    directions_result = gmaps.directions(start,
                                         end,
                                         mode="walking",
                                         departure_time=now, 
                                         alternatives=False
                                         )
    
    duration = directions_result[0]["legs"][0]["duration"]["value"]  # in seconds
    distance = directions_result[0]["legs"][0]["distance"]["value"]  # in meters
    polyline = directions_result[0]["overview_polyline"]["points"]

    if not polyline:
        raise HTTPException(status_code=400, detail="No polyline found")
    try:
        
        route = RouteDB(
           user_id=current_user.username,
           start_ll=start,
           start_address=directions_result[0]["legs"][0]["start_address"],
           end_address=directions_result[0]["legs"][0]["end_address"],
           duration = duration,
           distance = distance,
           end_ll=end,
           polyline=polyline
        )
        db.add(route)
        db.commit()
        db.refresh(route)

        route_pyd = RoutePyd(
            start_ll=route.start_ll,
            end_ll=route.end_ll,
            duration=route.duration,
            distance=route.distance,
            polyline=route.polyline,
            start_address=route.start_address,
            end_address=route.end_address
        )
        
        publish_tracking_task(TrackingTaskMessage(uid=current_user.username, 
                                                  device_id='temp_id',
                                                  action=TrackingTaskAction.START, 
                                                  polyline=route.polyline
                                                  )
                             )
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
        
    return route_pyd

@router.post('/delete')
async def delete_current_route(
    current_user: Annotated[UserPyd, Depends(get_current_user)],
    db: db_dependency
):

    try:
       message =  await delete_users_route(current_user.username, db)
       return message
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete route")