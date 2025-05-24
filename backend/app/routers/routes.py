from datetime import datetime, timedelta
from typing import Annotated, Any

from dependencies import db_dependency, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.models.alchemy.route import Route as RouteDB
from app.models.pyd.user import RouteCreateRequest
from app.models.pyd.user import User as UserPyd
from app.pubsub.tracking_task import publish_tracking_task
from app.repositories.google_maps import get_google_maps_client
from app.schemas.route import mapModelToRouteDTO
from app.types.tracking import TrackingTaskAction, TrackingTaskMessage
from app.utils import delete_users_route

router = APIRouter()


class AddressModel(BaseModel):
    house_number: str
    street: str
    city: str
    postal_code: str


@router.post("/coordinates")
async def get_coordinates(
    address_model: AddressModel,
    current_user: Annotated[UserPyd, Depends(get_current_user)],
    gmaps: Annotated[Any, Depends(get_google_maps_client)],
):
    full_address = f"{address_model.house_number} {address_model.street}, {address_model.city}, {address_model.postal_code}"
    location = gmaps.geocode(full_address)

    if location:
        lat = location[0]["geometry"]["location"]["lat"]
        lng = location[0]["geometry"]["location"]["lng"]
        return {"lat": lat, "lng": lng}
    else:
        raise HTTPException(status_code=404, detail="Address not found")


@router.post("/create")
async def get_current_route(
    current_user: Annotated[UserPyd, Depends(get_current_user)],
    db: db_dependency,
    gmaps: Annotated[Any, Depends(get_google_maps_client)],
    request: RouteCreateRequest,
):
    try:
        current_route = (
            db.query(RouteDB).filter(RouteDB.user_id == current_user.username).first()
        )
        if current_route:
            return mapModelToRouteDTO(current_route)

    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

    now = datetime.now()
    start = request.start_ll
    end = request.end_ll
    directions_result = gmaps.directions(
        start, end, mode="walking", departure_time=now, alternatives=False
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
            duration=duration,
            distance=distance,
            end_ll=end,
            polyline=polyline,
        )
        db.add(route)
        db.commit()
        db.refresh(route)

        route_dto = mapModelToRouteDTO(route)

        publish_tracking_task(
            TrackingTaskMessage(
                uid=current_user.username,
                device_id="temp_id",
                action=TrackingTaskAction.START,
                polyline=route.polyline,
                time_needed=timedelta(seconds=route.duration)
            )
        )

        return route_dto
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router.post("/delete")
async def delete_current_route(
    current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency
):
    try:
        message = await delete_users_route(current_user.username, db)
        return message
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete route",
        )
