from typing import Annotated
from app.models.pyd.user import  FriendAddRequest, UpdateUserModel
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship
from fastapi import APIRouter, Depends, HTTPException, Request, status
from settings import env

from dependencies import db_dependency

def validate_track_header(request: Request):
    header_value = request.headers.get("X-TRACK-API")
    if not header_value or header_value != env.TRACKING_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TRACK-API header"
        )
    return header_value

router = APIRouter()

@router.get('/emergency/tracking')
async def emergency_event(db: db_dependency, token: Annotated[str, Depends(validate_track_header)]):
    return {"validated": True};

@router.get('/completed')
async def emergency_event(db: db_dependency, token: Annotated[str, Depends(validate_track_header)]):
    return {"validated": True};



@router.get('/emergency/ui')
async def emergency_event(db: db_dependency, token: Annotated[str, Depends(validate_track_header)]):
   return {"validated": True};


@router.get('/completed/ui')
async def emergency_event(db: db_dependency, token: Annotated[str, Depends(validate_track_header)]):
   return {"validated": True};





