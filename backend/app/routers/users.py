from typing import Annotated

from dependencies import db_dependency, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.alchemy.user import User as UserDB
from app.models.pyd.user import UpdateUserModel
from app.models.pyd.user import User as UserPyd

router = APIRouter()


@router.get("/me")
async def read_auth_user(current_user: Annotated[UserPyd, Depends(get_current_user)]):
    return current_user


@router.post("/update")
async def update_user(
    update_model: UpdateUserModel,
    current_user: Annotated[UserPyd, Depends(get_current_user)],
    db: db_dependency,
):
    try:
        user = db.query(UserDB).filter(UserDB.username == current_user.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if update_model.new_name is not None:
            user.name = update_model.new_name
        if update_model.latitude is not None:
            user.latitude = update_model.latitude
        if update_model.longitude is not None:
            user.longitude = update_model.longitude
        if update_model.street is not None:
            user.street = update_model.street
        if update_model.city is not None:
            user.city = update_model.city
        if update_model.country is not None:
            user.country = update_model.country

        db.commit()
        db.refresh(user)

    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )

    return {
        "message": "User updated successfully",
        "updated_fields": update_model.dict(exclude_none=True),
    }
