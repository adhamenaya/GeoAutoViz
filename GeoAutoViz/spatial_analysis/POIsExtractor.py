from abc import ABC
import osmnx as ox

from GeoAutoViz.interfaces.DataExtractor import DataExtractor
from GeoAutoViz.GeoUtils import GeoUtils


class POIsExtractor(DataExtractor, ABC):

    def __init__(self):
        super().__init__()
        self.distance = 700

    def extract(self):
        pass

    def get_pois_based_on_point(self, point, tags, distance):
        return ox.geometries_from_point(center_point=point, tags=tags, dist=distance)

    def get_pois_based_on_polygon(self, polygon, tags):
        return ox.geometries_from_polygon(polygon=polygon, tags=tags)

    def get_pois_by_tags(self, geo_param, tags, distance=0):
        if GeoUtils.is_geo_point(geo_param):
            return self.get_pois_based_on_point(point=(geo_param.x, geo_param.y), tags= tags, distance=distance)
        elif GeoUtils.is_geo_polygon(geo_param):
            return self.get_pois_based_on_polygon(geo_param, tags=tags)

    def get_buildings(self, geo_param, distance=0):
        tags = {"building": True}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_residential(self, geo_param, distance=0):
        tags={"building": ['house', 'residential', 'apartments']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_commercial(self, geo_param, distance=0):
        tags={'building': ['retail', 'office', 'commercial', 'supermarket', 'industrial', 'warehouse']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_leisure(self, geo_param, distance=0):
        tags={'leisure': ['amusement_arcade', 'dance', 'fitness_centre', 'fitness_station', 'garden', 'park', 'playground']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_green_spaces(self, geo_param, distance=0):
        tags={'leisure': ['garden', 'park', 'playground']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_sports(self, geo_param, distance=0):
        tags={'leisure': ['sports_centre', 'stadium', 'swimming_area', 'swimming_pool']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_educational(self, geo_param, distance=0):
        tags={'amenity': ['college', 'kindergarten', 'school', 'university']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_healthcare(self, geo_param, distance=0):
        tags={'amenity': ['clinic', 'dentist', 'pharmacy', 'doctors', 'hospital']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_sustenance(self, geo_param, distance=0):
        tags={'amenity': ['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'pub', 'ice_cream', 'restaurant']}
        return self.get_pois_by_tags(geo_param, tags, distance)

    def get_religious(self, geo_param, distance=0):
        tags={'amenity': ['place_of_worship']}
        return self.get_pois_by_tags(geo_param, tags, distance)
