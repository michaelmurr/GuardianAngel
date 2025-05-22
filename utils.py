import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status

from models.alchemy.user import User
from models.pyd.user import UserInDB

SECRET = "692231733f2092790aff8c5aa3a874480775d5c241cf09de0a876344350abf70"
GOOGLE_WEB_CLIENT_ID = "615112230301-vid38eo6tkpu2bps9h648t2s8i7b46p2.apps.googleusercontent.com"
GOOGLE_IOS_CLIENT_ID = "615112230301-crgaciahtdvjpbir4jdmma4i9dkksetu.apps.googleusercontent.com"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 90

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def veryfy_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)



def get_password_hash(password):
        return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db):
        user = db.query(User).filter(User.username == username).first()
        if not user: 
                return None
        if not veryfy_password(password, user.hashed_password):
                return None
        return UserInDB(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
        

def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
                expire = datetime.utcnow() + expires_delta
        else:
                expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
        return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
                expire = datetime.utcnow() + expires_delta
        else:
                expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
        return encoded_jwt

async def decode_token(token: str, db) -> UserInDB | None:
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
                )   
        try:
               payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
               username = payload.get("sub")
              
               if username is None:
                       raise credentials_exception
        except jwt.InvalidTokenError:
                raise credentials_exception       
        user_from_db = db.query(User).filter(User.username == username).first()
        if not user_from_db:
                return None
        return UserInDB(username=user_from_db.username, email=user_from_db.email, id=user_from_db.id, name=user_from_db.name, picture=user_from_db.picture)