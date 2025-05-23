from datetime import datetime
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

class NameChange(BaseModel):
    new_name : str

class Coordinates(BaseModel):
    latitude : float
    longitude : float

class Address(BaseModel):
    street : str
    city : str
    country : str