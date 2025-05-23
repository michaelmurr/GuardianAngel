from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    name: str | None = None
    street : str | None = None
    city : str | None = None
    country : str | None = None
    latitude : float | None = None
    longitude : float | None = None
    picture: str | None = None
  
class UserInDB(User):
    hashed_password: str | None = None
    id: str | None = None

class UpdateUserModel(BaseModel):
    new_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class FriendAddRequest(BaseModel):
    friend_username: str

class RouteCreateRequest(BaseModel):
    start_ll: str
    end_ll: str
