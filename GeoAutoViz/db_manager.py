# Imports
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import geopandas as gpd
from shapely import Point


class DBManager:

    def __init__(self, city):
        super().__init__()
        self.city = city.lower()
        self.engine = create_engine('postgresql://postgres:root@localhost:5432/urban_morphology')

    def save_buildings(self, gdf_buildings):
        gdf_buildings.to_postgis(self.city + "_building", self.engine, if_exists='append')

    def save_tessellations(self, gdf_tessellations):
        gdf_tessellations.to_postgis(self.city + "_tessellation", self.engine, if_exists='append')

    def save_streets(self, gdf_streets):
        gdf_streets.to_postgis(self.city + "_street", self.engine, if_exists='append')

    def save_urban_types(self, gdf_urban_types):
        gdf_urban_types.to_postgis(self.city + "_urban_types", self.engine, if_exists='append')

    def read_buildings(self):
        query = 'SELECT *, geometry AS geom FROM ' + self.city + "_building"
        gdf = gpd.GeoDataFrame.from_postgis(query, self.engine)
        return gdf

    def read_streets(self):
        query = 'SELECT *, geometry AS geom FROM ' + self.city + "_street"
        gdf = gpd.GeoDataFrame.from_postgis(query, self.engine)
        return gdf

    def read_tessellations(self):
        query = 'SELECT *, geometry AS geom FROM ' + self.city + "_tessellation"
        gdf = gpd.GeoDataFrame.from_postgis(query, self.engine)
        return gdf

    def read_urban_types(self):
        query = 'SELECT *, geometry AS geom FROM ' + self.city + "_urban_type"
        gdf = gpd.GeoDataFrame.from_postgis(query, self.engine)
        return gdf
