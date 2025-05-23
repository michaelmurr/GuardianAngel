from typing import Annotated

from dependencies import db_dependency
from fastapi import APIRouter, Depends, HTTPException, Request, status
from settings import env


def validate_track_header(request: Request):
    header_value = request.headers.get("X-TRACK-API")
    if not header_value or header_value != env.TRACKING_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TRACK-API header",
        )
    return header_value


router = APIRouter()


@router.get("/emergency/tracking")
async def tracking_emergency_event(
    db: db_dependency, token: Annotated[str, Depends(validate_track_header)]
):
    return {"validated": True}


@router.get("/completed")
async def completed_event(
    db: db_dependency, token: Annotated[str, Depends(validate_track_header)]
):
    return {"validated": True}


@router.get("/emergency/ui")
async def ui_emergency_event(
    db: db_dependency, token: Annotated[str, Depends(validate_track_header)]
):
    return {"validated": True}
