
from datetime import datetime
from pydantic import BaseModel


class HostedGame(BaseModel):
        title: str
        startDate: datetime | None = None
        isActive: bool 
        host: str | None = None
        
        class Config:
                from_attributes = True