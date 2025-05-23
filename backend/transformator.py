from typing import List

import polyline
from app.types.general import Location
from pyproj import Transformer
from shapely import LineString, Point, Polygon
from shapely.geometry import mapping
from shapely.ops import transform


class GeoTransformator:
    _to_m_transformer: Transformer = Transformer.from_crs(
        "EPSG:4326", "EPSG:3857", always_xy=True
    )
    _to_deg_transformer: Transformer = Transformer.from_crs(
        "EPSG:3857", "EPSG:4326", always_xy=True
    )

    @staticmethod
    def decode_polyline(str_polyline: str) -> List[Location]:
        coords: List[tuple[float, float]] = polyline.decode(str_polyline)
        route = [Location(latitude=lat, longitude=lon) for lat, lon in coords]
        return route

    @staticmethod
    def calculate_corridor_from_route(
        route: List[Location], buffer_meters: float = 80.0
    ) -> Polygon:
        """
        Create a safe coridor based on the user's route (array of locations)

        :param polyline: Geo-polyline
        :param buffer_meters: Width of buffer zone in meters
        :return: True if user is on route, False if off-route
        """

        # Convert route to LineString (lon, lat)
        line = LineString([(loc.longitude, loc.latitude) for loc in route])
        # Project to Web Mercator (meters) for accurate buffering
        line_m = transform(GeoTransformator._to_m_transformer.transform, line)
        # Buffer and containment check
        corridor = line_m.buffer(buffer_meters)

        return corridor

    @staticmethod
    def calculate_finish_from_location(
        destination: Location, radius: float = 50.0
    ) -> Polygon:
        dest_point_m = GeoTransformator.calculate_point_from_location(destination)
        destination_area = dest_point_m.buffer(radius)
        return destination_area

    @staticmethod
    def calculate_point_from_location(location: Location):
        point = Point(location.longitude, location.latitude)
        point_m = transform(GeoTransformator._to_m_transformer.transform, point)
        return point_m

    @staticmethod
    def is_user_in_route_corridor(corridor: Polygon, user_location: Location) -> bool:
        """
        Check if user's location is within a buffered corridor of the route.

        :param user_location: Location object (longitude, latitude)
        :return: True if user is on route, False if off-route
        """

        point = Point(user_location.longitude, user_location.latitude)
        point_m = transform(GeoTransformator._to_m_transformer.transform, point)
        return corridor.contains(point_m)

    @staticmethod
    def corridor_to_geojson(corridor_geom: Polygon):
        """
        Convert a buffered corridor geometry to GeoJSON format.

        :param corridor_geom: Shapely geometry in projected (meter) coordinates
        :return: GeoJSON dict
        """

        # Old code
        # line_m = transform(transformer.transform, line)
        # buffer_m = line_m.buffer(buffer_meters)

        # # Transform buffer back to WGS84 (lat/lon)
        # buffer_wgs = transform(to_deg, buffer_m)
        # geojson_dict = buffer_wgs.__geo_interface__
        # import json

        # with open("buffer.geojson", "w") as f:
        #     json.dump(geojson_dict, f)

        # Reproject back to WGS84 (lat/lon)
        corridor_wgs = transform(
            GeoTransformator._to_deg_transformer.transform, corridor_geom
        )

        # Convert to GeoJSON dictionary
        geojson = {
            "type": "Feature",
            "properties": {"name": "Safe Corridor"},
            "geometry": mapping(corridor_wgs),
        }
        return geojson
