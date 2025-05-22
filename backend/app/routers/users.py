

from typing import Annotated
from app.models.pyd.user import UserInDB

from fastapi import APIRouter, Depends

from dependencies import get_current_user



router = APIRouter()



@router.get('/me', response_model=UserInDB)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
       return current_user

