
from pydantic import BaseModel

class Route(BaseModel):
    start_ll: str
    end_ll: str
    duration: int | None
    distance: int | None
    polyline: str
    start_address: str
    end_address: str