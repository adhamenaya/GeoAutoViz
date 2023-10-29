import math

import networkx as nx
import osmnx as ox  # (optional, for fetching OpenStreetMap data)
from shapely import Point


class ZoneAreaAnalyzer:
    def __init__(self, extractor, distance=700):
        super().__init__()
        self.distance = distance
        self.extractor = extractor

    def calculate_entropy(self, pois_density_row):
        p_sum = 0
        for i in range(1, len(pois_density_row)):  # start from 1 to exclude 'buildings' which is already included!!
            lnd_use_percent = round(pois_density_row[i] / pois_density_row[0], 3)  # divide by/ index 0 for buildings
            lnd_use_percent = round(pois_density_row[i] / sum(pois_density_row[1:]), 3)  # divide by total of POIs
            if lnd_use_percent == 0:
                lnd_use_percent = 0.001
            p_sum = p_sum + lnd_use_percent * math.log(lnd_use_percent)
            k = len(pois_density_row) - 5 + 1
            entropy = -1 * (p_sum / math.log(k))
        return round(entropy, 3)

    def extract_pois_density_around_point(self, lat, lon, distance):
        buildings = len(self.extractor.get_buildings(Point(lat, lon), distance=distance))
        residential = len(self.extractor.get_residential(Point(lat, lon), distance=distance))
        commercial = len(self.extractor.get_commercial(Point(lat, lon), distance=distance))
        sustenance = len(self.extractor.get_sustenance(Point(lat, lon), distance=distance))
        leisure = len(self.extractor.get_leisure(Point(lat, lon), distance=distance))
        #green_spaces = len(self.extractor.get_green_spaces(Point(lat, lon), distance=distance))
        public_service = len(self.extractor.get_public_service(Point(lat, lon), distance=distance))
        business = len(self.extractor.get_business(Point(lat, lon), distance=distance))

        return list(
            map(lambda x: x + 1,
                [buildings, residential, commercial, sustenance, leisure, business, public_service]))

    def extract_pois_density_in_polygon(self, polygon):
        buildings = len(self.extractor.get_buildings(polygon))
        residential = len(self.extractor.get_residential(polygon))
        commercial = len(self.extractor.get_commercial(polygon))
        sustenance = len(self.extractor.get_sustenance(polygon))
        leisure = len(self.extractor.get_leisure(polygon))
        #green_spaces = len(self.extractor.get_green_spaces(polygon))
        public_service = len(self.extractor.get_public_service(polygon))
        business = len(self.extractor.get_business(polygon))

        return list(
            map(lambda x: x + 1,
                [buildings, residential, commercial, sustenance, leisure, business, public_service]))

    def get_classified_buildings(self, polygon, df_classes):

        # poi_classes = {"building": 1,
        #                "residential": 2,
        #                "commercial": 3,
        #                "sustenance": 4,
        #                "business": 5,
        #                "public_service": 6,
        #                "green_spaces": 7,
        #                "leisure": 8
        #                }

        building2 = self.extractor.get_buildings(polygon)
        building2["osmid"] = building2.index.get_level_values(1)
        residential = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 2]["osmid"])])
        commercial = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 3]["osmid"])])
        sustenance = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 4]["osmid"])])
        business = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 5]["osmid"])])
        public_service = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 6]["osmid"])])
        #ßgreen_spaces = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 7]["osmid"])])
        leisure = len(building2[building2["osmid"].isin(df_classes[df_classes["class"] == 8]["osmid"])])

        return list(
            map(lambda x: x + 1,
                [len(building2), residential, commercial, sustenance, leisure, green_spaces, business, public_service]))

    def calculate_service_area(self, city_name, origin, impedance_type):
        # Create a graph using OpenStreetMap data
        graph = ox.graph_from_place(city_name, network_type="all")

        # Calculate service area
        if impedance_type not in ["length", "time"]:
            raise ValueError("Impedance type must be 'length' or 'time'")

        if impedance_type == "time":
            impedance = "travel_time"
        else:
            impedance = "length"

        service_area = nx.shortest_path_length(graph, source=origin, weight=impedance)

        return service_area
