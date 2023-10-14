import math

import networkx as nx
import osmnx as ox  # (optional, for fetching OpenStreetMap data)


class CatchmentAreaAnalyzer:
    def __init__(self, distance=700):
        super().__init__()
        self.distance = distance

    def get_buildings(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={"building": True},
                                        dist=self.distance)

    def get_residential(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={"building": ['house', 'residential', 'apartments']},
                                        dist=self.distance)

    def get_commercial(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'building': ['retail', 'office', 'commercial',
                                                           'supermarket', 'industrial', 'warehouse']},
                                        dist=self.distance)

    def get_leisure(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'leisure': ['amusement_arcade', 'dance',
                                                          'fitness_centre', 'fitness_station',
                                                          'garden', 'park', 'playground']},
                                        dist=self.distance)

    def get_green_spaces(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'leisure': ['garden', 'park', 'playground']},
                                        dist=self.distance)

    def get_sports(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'leisure': ['sports_centre', 'stadium', 'swimming_area',
                                                          'swimming_pool']},
                                        dist=self.distance)

    def get_educational(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'amenity': ['college', 'kindergarten', 'school', 'university']},
                                        dist=self.distance)

    def get_healthcare(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'amenity': ['clinic', 'dentist', 'pharmacy',
                                                          'doctors', 'hospital']},
                                        dist=self.distance)

    def get_sustenance(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'amenity': ['bar', 'biergarten', 'cafe', 'fast_food',
                                                          'food_court', 'pub', 'ice_cream', 'restaurant']},
                                        dist=self.distance)

    def get_religious(self, lat, lon):
        return ox.geometries_from_point(center_point=(lat, lon),
                                        tags={'amenity': ['place_of_worship']},
                                        dist=self.distance)

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
        buildings = len(self.get_buildings(lat, lon))
        residential = len(self.get_residential(lat, lon))
        commercial = len(self.get_commercial(lat, lon))
        leisure = len(self.get_leisure(lat, lon))
        green_spaces = len(self.get_green_spaces(lat, lon))
        sports = len(self.get_sports(lat, lon))
        educational = len(self.get_educational(lat, lon))
        healthcare = len(self.get_healthcare(lat, lon))
        sustenance = len(self.get_sustenance(lat, lon))
        religious = len(self.get_religious(lat, lon))

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