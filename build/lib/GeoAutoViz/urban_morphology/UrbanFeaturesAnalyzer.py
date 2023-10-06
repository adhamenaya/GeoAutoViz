# GeoPandas: https://geopandas.org/
# Fiona: https://fiona.readthedocs.io/en/latest/
# Shapely: https://shapely.readthedocs.io/en/stable/
# GDAL (Geospatial Data Abstraction Library): https://gdal.org/
# Rasterio: https://rasterio.readthedocs.io/en/latest/
# Pyproj: https://pyproj4.github.io/pyproj/stable/
# Basemap (Matplotlib Toolkit): https://matplotlib.org/basemap/
# Cartopy: https://scitools.org.uk/cartopy/docs/latest/
# Rtree: https://toblerity.org/rtree/
# GeoAlchemy: https://geoalchemy-2.readthedocs.io/en/latest/

import warnings

import libpysal
import momepy
import pandas
from clustergram import Clustergram

from db_manager import DBManager

from GeoAutoViz.interfaces.DataAnalyzer import DataAnalyzer


class UrbanFeaturesAnalyzer(DataAnalyzer):
    def __init__(self, datasource=None):
        super().__init__()

        self.streets = None
        self.tessellations = None
        self.buildings = None

        self.datasource = datasource

        self.streets_nodes = None
        self.place = datasource.place

        if datasource.db_name is None:
            self.db_name = datasource.place
        else:
            self.db_name = datasource.db_name

        self.db = DBManager(self.db_name)
        self.local_crs = datasource.local_crs

        # neighbors wights
        self.queen_1 = None
        self.queen_3 = None

        # merge all datasets
        self.merged = None
        self.percentiles_joined = None
        self.percentiles_standardized = None
        self.urban_types = None

    def setup(self):
        self.buildings = self.datasource.buildings
        self.tessellations = self.datasource.tessellations
        self.streets = self.datasource.streets

        self.merge_buildings_streets()
        self.merge_buildings_tessellations()

    def read_buildings(self):
        print("Reading buildings from the database...")
        self.buildings = self.db.read_buildings()
        return self.buildings

    def read_tessellations(self):
        print("Reading tessellations from the database...")
        self.tessellations = self.db.read_tessellations()
        return self.tessellations

    def read_streets(self):
        print("Reading streets from the database...")
        self.streets = self.db.read_streets()
        return self.streets

    def merge_buildings_streets(self, max_distance=1000):
        print("Merging buildings and streets...")
        self.buildings = self.buildings.sjoin_nearest(self.streets, max_distance=max_distance, how='left')
        self.buildings = self.buildings.drop_duplicates("uID").drop(columns='index_right')

    def merge_buildings_tessellations(self):
        print("Merging buildings and tessellations...")
        self.tessellations = self.tessellations.merge(self.buildings[['uID', 'nID']], on='uID', how='left')

    def compute_buildings_area(self):
        print("Computing buildings' area...")
        self.buildings["area"] = self.buildings.area

    def compute_tessellation_area(self):
        print("Computing tessellation area...")
        self.tessellations["area"] = self.tessellations.area

    def compute_street_length(self):
        print("Computing street length...")
        self.streets["length"] = self.streets.length

    def compute_building_eri(self):
        print("Computing building's Equivalent Rectangular Index (ERI)...")
        self.buildings["eri"] = momepy.EquivalentRectangularIndex(self.buildings).series

    def compute_building_elongation(self):
        print("Computing building's elongation...")
        self.buildings["elongation"] = momepy.Elongation(self.buildings).series

    def compute_building_convexity(self):
        print("Computing building's convexity...")
        self.buildings["convexity"] = momepy.Convexity(self.tessellations).series

    def compute_streets_linearity(self):
        print("Computing street linearity...")
        self.streets["linearity"] = momepy.Linearity(self.streets).series

    def compute_building_shared_walls(self):
        print("Computing building's shared walls ratio...")
        self.buildings["shared_walls"] = momepy.SharedWallsRatio(self.buildings).series

    def setup_neighbors(self):
        """
        ids="uID" is the unique ID of spatial unit, and "queen_1" represents the spatial wight matrix using the queen
        continuity criterion. "queen_3" generates spatial weights based on a higher order criterion (=3).
        :return:
        """
        print("Setting up neighbors...")
        self.queen_1 = libpysal.weights.contiguity.Queen.from_dataframe(self.tessellations, ids="uID",
                                                                        silence_warnings=True)
        self.queen_3 = momepy.sw_high(k=3, weights=self.queen_1)

    def compute_tessellation_neighbors(self):
        print("Computing tessellation neighbors...")
        self.tessellations["neighbors"] = momepy.Neighbors(self.tessellations, self.queen_1, "uID", weighted=True,
                                                           verbose=False).series

    def compute_tessellation_covered_area(self):
        print("Computing tessellation covered area...")
        self.tessellations["covered_area"] = momepy.CoveredArea(self.tessellations, self.queen_1, "uID",
                                                                verbose=False).series

    def compute_building_neighbor_distance(self):
        print("Computing building's neighbor distance...")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.buildings["neighbor_distance"] = momepy.NeighborDistance(self.buildings, self.queen_1, "uID",
                                                                          verbose=False).series

    def compute_building_interbuilding_distance(self):
        self.setup_neighbors()
        print("Computing building's interbuilding distance...")
        self.buildings["interbuilding_distance"] = momepy.MeanInterbuildingDistance(self.buildings, self.queen_1, "uID",
                                                                                    self.queen_3, verbose=False).series

    def compute_building_adjacency(self):
        self.setup_neighbors()
        print("Computing building adjacency...")
        buildings_q1 = libpysal.weights.contiguity.Queen.from_dataframe(self.buildings, silence_warnings=True)
        self.buildings["adjacency"] = momepy.BuildingAdjacency(self.buildings, self.queen_3, "uID", buildings_q1,
                                                               verbose=False).series

    def get_street_pofile(self):
        return momepy.StreetProfile(self.streets, self.buildings)

    def compute_street_width(self):
        print("Computing street width...")
        self.streets["width"] = self.get_street_pofile().w

    def compute_street_width_deviation(self):
        print("Computing street width deviation...")
        self.streets["width_deviation"] = self.get_street_pofile().wd

    def compute_street_openness(self):
        print("Computing street openness...")
        self.streets["openness"] = self.get_street_pofile().o

    def compute_tessellation_car(self):
        print("Computing tessellation car ratio...")
        self.tessellations["car"] = momepy.AreaRatio(self.tessellations, self.buildings, "area", "area", "uID").series

    def compute_street_closeness_centrality(self):
        print("Computing street closeness and meshedness...")
        graph = momepy.gdf_to_nx(self.streets)
        graph = momepy.node_degree(graph)
        graph = momepy.closeness_centrality(graph, radius=400, distance="mm_len")
        graph = momepy.meshedness(graph, radius=400, distance="mm_len")
        self.streets_nodes, self.streets = momepy.nx_to_gdf(graph)

    def merge_buildings_nodes(self):
        print("Merging buildings and nodes...")
        self.buildings["nodeID"] = momepy.get_node_id(self.buildings, self.streets_nodes, self.streets, "nodeID", "nID")

    def merge_all_datasets(self):
        print("Merging all datasets...")
        self.merged = self.tessellations.merge(self.buildings.drop(columns=["nID", "geometry"]), on="uID")
        self.merged = self.merged.merge(self.streets.drop(columns="geometry"), on="nID", how="left")
        self.merged = self.merged.merge(self.streets_nodes.drop(columns="geometry"), on="nodeID", how="left")
        return self.merged

    def compute_merged_percentiles(self):
        self.merge_buildings_nodes()
        self.merge_all_datasets()
        self.setup_neighbors()

        print("Computing merged percentiles...")
        percentiles = []
        for column in self.merged.columns.drop(
                ["uID", "nodeID", "nID", 'mm_len', 'node_start', 'node_end', "geometry"]):
            perc = momepy.Percentiles(self.merged, column, self.queen_3, "uID", verbose=False).frame
            perc.columns = [f"{column}_" + str(x) for x in perc.columns]
            percentiles.append(perc)

        self.percentiles_joined = pandas.concat(percentiles, axis=1)

    def compute_standardized_percentiles(self):
        print("Computing standardized percentiles...")
        self.percentiles_standardized = (self.percentiles_joined - self.percentiles_joined.mean()) / \
                                        self.percentiles_joined.std()

    def do_clustering(self, labels_count=4):
        print(f"Performing clustering with {labels_count} labels...")
        cgram = Clustergram(range(1, 12), n_init=10, random_state=42)
        cgram.fit(self.percentiles_standardized.fillna(0))
        self.merged["cluster"] = cgram.labels[labels_count].values
        self.urban_types = self.buildings[["geometry", "uID"]].merge(self.merged[["uID", "cluster"]], on="uID")

    def save_urban_types_to_db(self):
        print("Saving urban types to the database...")
        self.db.save_urban_types(self.urban_types)

    def read_urban_types(self):
        print("Reading urban types from the database...")
        self.urban_types = self.db.read_urban_types()
        return self.urban_types

    def prepare_data_for_clustering(self):
        self.compute_buildings_area()
        self.compute_tessellation_area()
        self.compute_street_length()
        self.compute_building_eri()
        self.compute_building_elongation()
        self.compute_building_convexity()
        self.compute_streets_linearity()
        self.compute_building_shared_walls()

        self.compute_tessellation_neighbors()
        self.compute_tessellation_covered_area()
        self.compute_building_neighbor_distance()
        self.compute_building_interbuilding_distance()
        self.compute_building_adjacency()
        self.compute_street_width()
        self.compute_street_width_deviation()
        self.compute_street_openness()
        self.compute_tessellation_car()
        self.compute_street_closeness_centrality()
        self.compute_merged_percentiles()
        self.compute_standardized_percentiles()

        self.do_clustering()

