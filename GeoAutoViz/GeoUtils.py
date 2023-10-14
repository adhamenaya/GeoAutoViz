from shapely import Point


class GeoUtils:
    def is_point_inside_polygon(lat, lon, polygon):
        return polygon.contains(Point(lon, lat))