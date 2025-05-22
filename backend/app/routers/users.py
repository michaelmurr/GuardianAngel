

from typing import Annotated
from app.models.pyd.user import UserInDB

from fastapi import APIRouter, Depends

from dependencies import get_current_user



router = APIRouter()



@router.get('/me')
async def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
       return current_user

