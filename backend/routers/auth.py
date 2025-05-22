
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,  status
from fastapi.security import OAuth2PasswordRequestForm

from models.pyd.user import IdToken, RefreshToken, UserInDB
from dependencies import db_dependency
from models.alchemy.user import User
from models.pyd.user import UserIn, UserInDB
from utils import ACCESS_TOKEN_EXPIRE_MINUTES, GOOGLE_WEB_CLIENT_ID,GOOGLE_IOS_CLIENT_ID, REFRESH_TOKEN_EXPIRE_DAYS, authenticate_user, create_access_token, create_refresh_token, decode_token, get_password_hash
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(
    tags=["auth"],
)


@router.post('/token', description="Get access token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
               raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data= {"sub" : user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(data={"sub": user.username, "refresh": True}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/register", description="Register a new user")
async def register(user: UserIn, db: db_dependency):
    # check if user already exists
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

     # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": db_user.username, "refresh": True},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "username": db_user.username,
            "email": db_user.email
        }
    }

@router.post('/refresh')
async def refresh_access_token(refresh_token: RefreshToken, db: db_dependency):
       user = await decode_token(refresh_token.refresh_token, db)
       if not user:
           raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid authentication credentials",
           headers={"WWW-Authenticate": "Bearer"},
           )

       access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
       return {"access_token": access_token, "token_type": "bearer"} 


@router.post("/auth/google")
def verify_id_token(token: IdToken, db: db_dependency):
    try:
        # Verify and decode the token
        id_info = id_token.verify_oauth2_token(
            token.id_token,
            requests.Request(),
            [GOOGLE_WEB_CLIENT_ID, GOOGLE_IOS_CLIENT_ID]
        )

        #  Checking issuer
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user = db.query(User).filter_by(username=id_info["sub"]).first()

        if not user:
            db_user = User(
                username=id_info["sub"],
                email=id_info["email"],
                name=id_info.get("name"),
                picture=id_info.get("picture"),
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            

        access_token = create_access_token(data={"sub": id_info["sub"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(data={"sub": id_info["sub"], "refresh": True}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))