from typing import List

from app.models.alchemy.route import Route
from app.schemas.geo_json import GeoJson
from app.services.geo_service import GeoService
from app.types.general import Location
from pydantic import BaseModel


class LatLng(BaseModel):
    latitude: float
    longitude: float


class RouteDTO(BaseModel):
    start_ll: str
    end_ll: str
    duration: int | None
    distance: int | None
    coordinates: List[LatLng]
    geoJson: GeoJson
    start_address: str
    end_address: str


def mapToLatLng(loc: Location) -> LatLng:
    return LatLng(latitude=loc.latitude, longitude=loc.longitude)


def mapModelToRouteDTO(route: Route) -> RouteDTO:
    decoded_polyline = GeoService.decode_polyline(route.polyline)
    list_lat_lng = [mapToLatLng(location) for location in decoded_polyline]

    polygon = GeoService.calculate_corridor_from_route(decoded_polyline)
    geo_json_raw = GeoService.corridor_to_geojson(polygon)
    geo_json = GeoJson(**geo_json_raw)

    return RouteDTO(
        start_ll=route.start_ll,
        end_ll=route.end_ll,
        duration=route.duration,
        distance=route.distance,
        coordinates=list_lat_lng,
        geoJson=geo_json,
        start_address=route.start_address,
        end_address=route.end_address,
    )
