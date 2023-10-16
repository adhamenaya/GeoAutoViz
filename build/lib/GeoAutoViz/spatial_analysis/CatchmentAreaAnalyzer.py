import math

import networkx as nx
import osmnx as ox  # (optional, for fetching OpenStreetMap data)


class CatchmentAreaAnalyzer:
    def __init__(self, extractor, distance=700):
        super().__init__()
        self.distance = distance
        self.extractor = extractor

    def calculate_entropy(self, pois_density_row):
        p_sum = 0
        for i in range(5, len(pois_density_row)):
            lnd_use_percent = round(pois_density_row[i]/pois_density_row[4],3) # index 4 for buildings
            print(lnd_use_percent)
            if lnd_use_percent == 0:
                lnd_use_percent = 0.001
            p_sum = p_sum + lnd_use_percent * math.log(lnd_use_percent)
            k = len(pois_density_row) - 5 + 1
            entropy = -1 * (p_sum / math.log(k))
        return round(entropy,3)

    def extract_pois_density(self, lat, lon, location_id, location_name):
        buildings = len(self.extractor.get_buildings(lat, lon))
        residential = len(self.extractor.get_residential(lat, lon))
        commercial = len(self.extractor.get_commercial(lat, lon))
        leisure = len(self.extractor.get_leisure(lat, lon))
        green_spaces = len(self.extractor.get_green_spaces(lat, lon))
        sports = len(self.extractor.get_sports(lat, lon))
        educational = len(self.extractor.get_educational(lat, lon))
        healthcare = len(self.extractor.get_healthcare(lat, lon))
        sustenance = len(self.extractor.get_sustenance(lat, lon))
        religious = len(self.extractor.get_religious(lat, lon))

        return [location_id, location_name, lat, lon, buildings, residential, commercial, leisure,
                green_spaces, sports, educational, healthcare, sustenance, religious]

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