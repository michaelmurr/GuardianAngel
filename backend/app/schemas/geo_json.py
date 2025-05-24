from typing import List

from pydantic import BaseModel


class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class Properties(BaseModel):
    name: str


class GeoJson(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry
