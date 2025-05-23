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
    friends = (
        db.query(UserDB)
        .join(friendship, UserDB.username == friendship.c.friend_id)
        .filter(friendship.c.user_id == current_user.username)
        .all()
    )

    return [
        {
            "username": friend.username,
            "name": friend.name,
            "email": friend.email,
            "picture": friend.picture,
            "city": friend.city,
            "country": friend.country,
        }
        for friend in friends
    ]

@router.post("/add")
async def add_friend(
    request: FriendAddRequest,
    current_user: Annotated[UserPyd, Depends(get_current_user)],
    db: db_dependency
):
    # Check that the user exists
    friend = db.query(UserDB).filter(UserDB.username == request.friend_username).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    # Prevent adding yourself
    if friend.username == current_user.username:
        raise HTTPException(status_code=400, detail="You cannot add yourself as a friend")

    # Check if friendship already exists
    already_friends = db.query(friendship).filter_by(
        user_id=current_user.username,
        friend_id=friend.username
    ).first()

    if already_friends:
        raise HTTPException(status_code=400, detail="Already added as a friend")

    insert = friendship.insert().values(
        user_id=current_user.username,
        friend_id=friend.username
    )

    try:
        db.execute(insert)
        db.commit()
        return {"detail": f"{friend.username} added as a friend"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add friend")
