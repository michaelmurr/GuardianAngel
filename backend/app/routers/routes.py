from typing import Annotated, Any
from app.models.pyd.user import  FriendAddRequest, UpdateUserModel
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship
from fastapi import APIRouter, Depends, HTTPException

from app.repositories.google_maps import get_google_maps_client
from dependencies import get_current_user
from dependencies import db_dependency


router = APIRouter()


@router.post('/pull')
async def get_current_route(current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency, gmaps: Annotated[Any , Depends(get_google_maps_client)]):
    return gmaps