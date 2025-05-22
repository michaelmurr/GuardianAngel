

from typing import Annotated
from fastapi import APIRouter, Depends

from dependencies import get_current_user
from models.pyd.user import UserInDB


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)



@router.get('/me', response_model=UserInDB)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
       return current_user

