from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from database import SessionLocal
from sqlalchemy.orm import Session

from models.pyd.user import UserInDB
from utils import decode_token



## DB Dependency
def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()

db_dependency = Annotated[Session, Depends(get_db)]





## Auth Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency) -> UserInDB:
        user = await decode_token(token, db)
        if not user:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
                )
        return user

