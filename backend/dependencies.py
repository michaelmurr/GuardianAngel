from typing import Annotated
from urllib.request import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from database import SessionLocal
from sqlalchemy.orm import Session


from fastapi import FastAPI
from clerk_backend_api import Clerk
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Clerk with your secret key
clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

## DB Dependency
def get_db():
        db = SessionLocal()
        try:
                yield db
        finally:
                db.close()

db_dependency = Annotated[Session, Depends(get_db)]


async def get_current_user(request: Request):
    # Extract the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    # Extract the token from the header
    token = auth_header.split("Bearer ")[1]

    try:
        # Verify the session token with Clerk
        session = await clerk.sessions.verify(token)
        return session
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token") from e
