from GeoAutoViz.interfaces.DataSource import DataSource

import warnings
import momepy
import osmnx
from GeoAutoViz.db_manager import DBManager


class PostGISDataSource(DataSource):
    def __init__(self, place, db_name=None, local_crs=5514):
        super().__init__()
        # Initialize PostGIS-specific attributes here
        super().__init__()

        warnings.filterwarnings("ignore")

        self.buildings = None
        self.tessellations = None
        self.streets = None
        self.streets_nodes = None
        self.place = place

        if db_name is None:
            self.db_name = place
        else:
            self.db_name = db_name

        self.db = DBManager(self.db_name)
        self.local_crs = local_crs

        # neighbors wights
        self.queen_1 = None
        self.queen_3 = None

        # merge all datasets
        self.merged = None
        self.percentiles_joined = None
        self.percentiles_standardized = None
        self.urban_types = None

    def extract_data(self):
        # Implement the extraction logic for PostGIS
        pass

    def extract_buildings(self, source=DataSource.Online, save_offline=False, mode=Offline.DB):
        if source == DataSource.Online:
            print("Extracting buildings...")
            self.buildings = osmnx.geometries.geometries_from_place(self.place, tags={'building': True})

            # get polygons only
            self.buildings = self.buildings[self.buildings.geom_type == 'Polygon'].reset_index(drop=True)

            # append extra attributes about buildings
            # self.buildings["city"] = self.place
            # self.buildings["centroid"] = self.buildings.centroid
            self.buildings = self.buildings[['geometry']].to_crs(self.local_crs)
            self.buildings["uID"] = range(len(self.buildings))
            if save_offline:
                if mode == Offline.DB:
                    self.save_buildings_to_db()
        elif source == DataSource.Offline:
            print("Reading buildings from the database...")
            self.buildings = self.db.read_buildings()

        return self.buildings

    def save_buildings_to_db(self):
        print("Saving buildings to the database...")
        self.db.save_buildings(self.buildings)

    def extract_tessellation(self, source=DataSource.Online, buffered_limit=100, save_offline=False, mode=Offline.DB):
        if source == DataSource.Online:
            print("Extracting tessellation...")
            limit = momepy.buffered_limit(self.buildings, buffered_limit)

            self.tessellations = momepy.Tessellation(self.buildings, "uID", limit, verbose=False, segment=1)
            self.tessellations = self.tessellations.tessellation
            if save_offline:
                if mode == Offline.DB:
                    self.save_tessellations_to_db()
        elif source == DataSource.Offline:
            print("Reading tessellations from the database...")
            self.tessellations = self.db.read_tessellations()

        return self.tessellations

    def save_tessellations_to_db(self):
        print("Saving tessellations to the database...")
        self.db.save_tessellations(self.tessellations)

    def extract_streets(self, source=DataSource.Online, network_type='drive', save_offline=False, mode=Offline.DB):
        if source == DataSource.Online:
            print("Extracting streets...")
            osm_graph = osmnx.graph_from_place(self.place, network_type=network_type)
            osm_graph = osmnx.projection.project_graph(osm_graph, to_crs=self.local_crs)
            self.streets = osmnx.graph_to_gdfs(
                osm_graph,
                nodes=False,
                edges=True,
                node_geometry=False,
                fill_edge_geometry=True
            )
            self.streets = momepy.remove_false_nodes(self.streets)
            self.streets = self.streets[["geometry"]]
            self.streets["nID"] = range(len(self.streets))

            if save_offline:
                if mode == Offline.DB:
                    self.save_streets_to_db()
        elif source == DataSource.Offline:
            print("Reading streets from the database...")
            self.streets = self.db.read_streets()

        return self.streets

    def save_streets_to_db(self):
        print("Saving streets to the database...")
        self.db.save_streets(self.streets)

    def extract_data(self, source=DataSource.Online, save_offline=False, mode=Offline.DB):
        self.extract_buildings(source, save_offline=save_offline, mode=mode)
        self.extract_streets(source, save_offline=save_offline, mode=mode)
        self.extract_tessellation(source, save_offline=save_offline, mode=mode)
