from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
import httpx
import jwt
from jwt.algorithms import RSAAlgorithm
import json
from app.models.alchemy.user import User
from settings import env
from app.models.pyd.user import UserInDB
from database import SessionLocal
from sqlalchemy.orm import Session
from clerk_backend_api import Clerk
from dotenv import load_dotenv
import os

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

def get_rsa_key_from_jwks(jwks, kid):
    """Extract the RSA public key from JWKS using the key ID"""
    for key in jwks.get('keys', []):
        if key.get('kid') == kid:
            return RSAAlgorithm.from_jwk(json.dumps(key))
    return None

async def get_current_user(request: Request, db: db_dependency):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header"
        )
    
    token = auth_header.split("Bearer ")[1]
    
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')
        
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing key ID"
            )
        
        jwks = await get_public_keys()
        rsa_key = get_rsa_key_from_jwks(jwks, kid)
        
        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key"
            )
        
        # Verify JWT token
        payload = jwt.decode(
            token,
            rsa_key,  
            algorithms=["RS256"],
            issuer=CLERK_ISSUER,  
            options={"verify_exp": True} 
        )
        
        # Extract user info from token
        user_id = payload.get("sub")
        username = payload.get("username") or payload.get("email") or user_id
        email = payload.get("email")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID"
            )
        
       
        user_pydantic = UserInDB(username=username, id=user_id, email=email)
        
       
        try:
           
            user_db = db.query(User).filter(User.username == user_id).first()

            if not user_db:
               
                user_db = User(
                    username=user_id,  
                    email=email
                )
                db.add(user_db)  
                db.commit()
                db.refresh(user_db) 
                
                print(f"Created new user: {user_id}")
            else:
                print(f"User already exists: {user_id}")
                
        except Exception as db_error:
           
            print(f"Database error (not auth error): {str(db_error)}")
            db.rollback()
            
        return user_pydantic  
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except HTTPException:
        # Re-raise HTTP exceptions (auth errors)
        raise
    except Exception as e:
        # ❌ CRITICAL FIX: Don't raise 401 for non-auth errors
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Alternative version that separates concerns better
async def get_current_user_clean(request: Request):
    """Authentication only - no database operations"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid Authorization header"
        )
    
    token = auth_header.split("Bearer ")[1]
    
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')
        
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing key ID"
            )
        
        jwks = await get_public_keys()
        rsa_key = get_rsa_key_from_jwks(jwks, kid)
        
        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key"
            )
        
        payload = jwt.decode(
            token,
            rsa_key,  
            algorithms=["RS256"],
            issuer=CLERK_ISSUER,  
            options={"verify_exp": True} 
        )
        
        user_id = payload.get("sub")
        username = payload.get("username") or payload.get("email") or user_id
        email = payload.get("email")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID"
            )
        
        return UserInDB(username=username, id=user_id, email=email)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

def create_or_get_user(user_data: UserInDB, db: Session):
    """Separate function for database operations"""
    try:
        user_db = db.query(User).filter(User.username == user_data.id).first()
        
        if not user_db:
            user_db = User(
                username=user_data.id,
                email=user_data.email
            )
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
            print(f"Created new user: {user_data.id}")
        
        return user_db
        
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )

# Usage in your routes:
# current_user = await get_current_user_clean(request)
# user_db = create_or_get_user(current_user, db)