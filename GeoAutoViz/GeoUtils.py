from shapely import Point, Polygon, MultiPolygon, wkt
import math


class GeoUtils:
    def is_point_inside_polygon(lat, lon, polygon):
        return polygon.contains(Point(lon, lat))

    def check_geometry_type(geo_param):
        if isinstance(geo_param, Point):
            return "Point"
        elif isinstance(geo_param, Polygon):
            return "Polygon"
        elif isinstance(geo_param, MultiPolygon):
            return "MultiPolygon"
        else:
            return "Unknown"

    def is_geo_multipolygon(geo_param):
        return GeoUtils.check_geometry_type(geo_param) == "MultiPolygon"

    def is_geo_point(geo_param):
        return GeoUtils.check_geometry_type(geo_param) == "Point"

    def is_geo_polygon(geo_param):
        return GeoUtils.check_geometry_type(geo_param) == "Polygon"

    def calculate_polygon_center(polygon):
        return polygon.centroid

    def calculate_haversine_distance(lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        radius = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius * c

        return distance

    def convert_multipolygon_to_list_of_polygons(multipolygon_param):
        multi =  MultiPolygon(multipolygon_param)
        return [p for p in multi.geoms]

    def is_valid_geometry(geom_text):
        try:
            # Attempt to create a Shapely geometry object from the WKT
            geom = wkt.loads(geom_text)
            # Check if the geometry is valid
            return geom.is_valid
        except Exception as e:
            # If there was an exception while creating the geometry, it is not valid
            return False