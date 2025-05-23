

from typing import Annotated
from app.models.pyd.user import  Address, Coordinates, NameChange
from app.models.pyd.user import User as UserPyd
from app.models.alchemy.user import User as UserDB
from fastapi import APIRouter, Depends, Body, HTTPException, status

from dependencies import get_current_user
from dependencies import db_dependency



router = APIRouter()


@router.get('/me')
async def read_auth_user(current_user: Annotated[UserPyd, Depends(get_current_user)]):
       return current_user



@router.post('/name')
async def change_name(name_model: NameChange, current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency):
    if name_model.new_name:
        try:
            user = db.query(UserDB).filter(UserDB.username == current_user.username).first()

            user.name = name_model.new_name
            db.commit()
            db.refresh(user)
        
        except Exception as e:
            db.rollback()
            print(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
    
        return name_model.new_name

    
    
@router.post("/coordinates")
async def update_cordinates(coordinates: Coordinates, current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency):
    try:
        user = db.query(UserDB).filter(UserDB.username == current_user.username).first()

        user.latitude = coordinates.latitude
        user.longitude = coordinates.longitude
        db.commit()
        db.refresh(user)
    
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    
    return coordinates

@router.post("/address")
async def update_cordinates(address_model: Address, current_user: Annotated[UserPyd, Depends(get_current_user)], db: db_dependency):
    try:
        user = db.query(UserDB).filter(UserDB.username == current_user.username).first()

        user.street = address_model.street
        user.city = address_model.city
        user.country = address_model.country
        db.commit()
        db.refresh(user)
    
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    
    return address_model