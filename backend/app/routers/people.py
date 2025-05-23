from typing import Annotated
from app.models.pyd.user import  FriendAddRequest, UpdateUserModel
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from app.models.alchemy.user import friendship
from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_current_user
from dependencies import db_dependency


router = APIRouter()

@router.get('/all')
async def get_my_added_friends(current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency):
    people = (
        db.query(UserDB)
        .filter(UserDB.username != current_user.username)
        .all()
    )

    return [
        {
            "username": person.username,
            "name": person.name,
            "email": person.email,
            "picture": person.picture,
            "city": person.city,
            "country": person.country,
        }
        for person in people
    ]