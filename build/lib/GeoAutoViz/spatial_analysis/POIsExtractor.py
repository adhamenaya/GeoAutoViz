from abc import ABC
import osmnx as ox
import pandas as pd

from GeoAutoViz.GeoUtils import GeoUtils

poi_classes = {"building": 1,
               "residential": 2,
               "commercial": 3,
               "sustenance": 4,
               "business": 5,
               "public_service": 6,
               "green_spaces": 7,
               "leisure": 8
               }


class POIsExtractor():

    def __init__(self):
        super().__init__()
        self.distance = 700

    def extract(self):
        pass

    def get_pois_based_on_point(self, point, tags, distance):
        return ox.geometries_from_point(center_point=point, tags=tags, dist=distance)

    def get_pois_based_on_polygon(self, polygon, tags):
        return ox.geometries_from_polygon(polygon=polygon, tags=tags)

    def get_pois_by_tags(self, geo_param, tags, distance=0, _class=None):
        data = pd.DataFrame()
        if GeoUtils.is_geo_point(geo_param):
            data = self.get_pois_based_on_point(point=(geo_param.x, geo_param.y), tags=tags, distance=distance)
        elif GeoUtils.is_geo_polygon(geo_param):
            data = self.get_pois_based_on_polygon(geo_param, tags=tags)
        data["class"] = _class
        return data

    def get_buildings(self, geo_param, distance=0):
        tags = {"building": True}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes["building"])

    def get_residential(self, geo_param, distance=0):
        tags = []
        tags.extend(['house', 'residential', 'apartments', 'hotel', 'dormitory'])
        tags = {"building": tags}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['residential'])

    def get_commercial(self, geo_param, distance=0):
        tags = []
        tags = {'shop': True}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['commercial'])

    def get_sustenance(self, geo_param, distance=0):
        tags = []
        # Class A3-A5 food and drinks
        tags.extend(['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'pub', 'ice_cream', 'restaurant'])
        tags = {'amenity': tags}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['sustenance'])

    def get_business(self, geo_param, distance=0):
        tags = []
        tags.extend(['warehouse', 'retail', 'supermarket'])
        tags.extend(['office', 'commercial', 'industrial', 'warehouse'])
        tags = {'building': tags}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['business'])

    def get_public_service(self, geo_param, distance=0):
        tags = []
        # Education
        tags.extend(['college', 'kindergarten', 'school', 'university'])
        # Healthcare
        tags.extend(['clinic', 'dentist', 'pharmacy', 'doctors', 'hospital'])
        # Religious
        tags.extend(['place_of_worship'])
        tags = {'amenity': tags}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['public_service'])

    def get_green_spaces(self, geo_param, distance=0):
        tags = {'leisure': ['garden', 'park', 'playground'],'landuse':['greenfield','grass']}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['green_spaces'])

    def get_leisure(self, geo_param, distance=0):
        tags = []
        # General leisure
        tags.extend(['amusement_arcade', 'dance', 'fitness_centre', 'fitness_station',
                     'garden', 'park', 'playground'])
        # Sports
        tags.extend(['sports_centre', 'stadium', 'swimming_area', 'swimming_pool'])
        tags = {'leisure': tags}
        return self.get_pois_by_tags(geo_param, tags, distance, poi_classes['leisure'])
