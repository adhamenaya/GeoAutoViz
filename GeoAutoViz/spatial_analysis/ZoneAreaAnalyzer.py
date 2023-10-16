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
        leisure = len(self.extractor.get_leisure(Point(lat, lon), distance=distance))
        green_spaces = len(self.extractor.get_green_spaces(Point(lat, lon), distance=distance))
        sports = len(self.extractor.get_sports(Point(lat, lon), distance=distance))
        educational = len(self.extractor.get_educational(Point(lat, lon), distance=distance))
        healthcare = len(self.extractor.get_healthcare(Point(lat, lon), distance=distance))
        sustenance = len(self.extractor.get_sustenance(Point(lat, lon), distance=distance))
        religious = len(self.extractor.get_religious(Point(lat, lon), distance=distance))

        return list(map(lambda x: x + 1, [buildings, residential, commercial, leisure, green_spaces,
                                          sports, educational, healthcare, sustenance, religious]))

    def extract_pois_density_in_polygon(self, polygon):
        buildings = len(self.extractor.get_buildings(polygon))
        residential = len(self.extractor.get_residential(polygon))
        commercial = len(self.extractor.get_commercial(polygon))
        leisure = len(self.extractor.get_leisure(polygon))
        green_spaces = len(self.extractor.get_green_spaces(polygon))
        sports = len(self.extractor.get_sports(polygon))
        educational = len(self.extractor.get_educational(polygon))
        healthcare = len(self.extractor.get_healthcare(polygon))
        sustenance = len(self.extractor.get_sustenance(polygon))
        religious = len(self.extractor.get_religious(polygon))

        return list(map(lambda x: x + 1, [buildings, residential, commercial, leisure, green_spaces,
                                          sports, educational, healthcare, sustenance, religious]))

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
