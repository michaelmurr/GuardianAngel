import os
from typing import Annotated

import httpx
import jwt
from app.models.alchemy.user import User
from app.models.pyd.user import User as UserPyd
from app.utils import get_rsa_key_from_jwks
from clerk_backend_api import Clerk
from database import SessionLocal
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from settings import env
from sqlalchemy.orm import Session

load_dotenv()

clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

## DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

cached_jwks = None
CLERK_ISSUER = "https://skilled-eft-62.clerk.accounts.dev"

async def get_public_keys():
    global cached_jwks
    if not cached_jwks:
        async with httpx.AsyncClient() as client:
            resp = await client.get(env.CLERK_JWKS_URL)
            cached_jwks = resp.json()
    return cached_jwks


security = HTTPBearer()


async def get_current_user(
    db: db_dependency, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing key ID"
            )

        jwks = await get_public_keys()
        rsa_key = get_rsa_key_from_jwks(jwks, kid)

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            issuer=CLERK_ISSUER,
            options={"verify_exp": True},
        )

        # Extract user info from token
        user_id = payload.get("sub")
        name = payload.get("name")
        email = payload.get("email")
        picture = payload.get("image")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user ID"
            )

        user_pydantic = UserPyd(username=user_id, email=email, name=name, picture=picture)

        user_pydantic = create_or_get_user(user_pydantic, db)

        return user_pydantic

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token issuer"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def create_or_get_user(user_data: UserPyd, db: Session):
    try:
        user_db = db.query(User).filter(User.username == user_data.username).first()

        if not user_db:
            user_db = User(username=user_data.username, email=user_data.email, name=user_data.name, picture=user_data.picture)
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
            print(f"Created new user: {user_data.username}")

        user_pydantic = UserPyd(
            username=user_db.username,
            email=user_db.email,
            name=user_db.name,
            street=user_db.street,
            city=user_db.city,
            country=user_db.country,
            latitude=user_db.latitude,
            longitude=user_db.longitude,
            picture=user_db.picture,
        )

        return user_pydantic

    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


async def verify_token_ws(token: str, db: db_dependency):
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing key ID"
            )

        jwks = await get_public_keys()
        rsa_key = get_rsa_key_from_jwks(jwks, kid)

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            issuer=CLERK_ISSUER,
            options={"verify_exp": True},
        )

        user_id = payload.get("sub")
        name = payload.get("name")
        email = payload.get("email")

        user_pydantic = UserPyd(username=user_id, email=email, name=name)

        user_pydantic = create_or_get_user(user_pydantic, db)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing user ID"
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token issuer"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
