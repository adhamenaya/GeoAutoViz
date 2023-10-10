# Geopandas - https://lnkd.in/dfJbwYTf
# Folium - https://lnkd.in/dAZM3CQm
# Cartopy - https://lnkd.in/dc8ijXRg
# Basemap - https://www.basemap.com
# Plotly - https://lnkd.in/dxbQCw6X
# Bokeh - https://bokeh.org
# PySAL - https://pysal.org
# Seaborn - https://seaborn.pydata.org
# Matplotlib - https://matplotlib.org
# Geoviews - https://geoviews.org
# Plotnine - https://plotnine.readthedocs.io/en/stable/
#
# Contextily - https://lnkd.in/dTdQsmKX
# Datashader - https://datashader.org
# Geemap - https://geemap.org
# Google Earth - https://lnkd.in/dXZdZc-g
# IPyleaflet - https://lnkd.in/dZtHigT4
# Kepler.gl - https://kepler.gl
# Leafmap - https://leafmap.org
# Mapwidget - https://lnkd.in/dy4JZzsz
# OSMNx - https://lnkd.in/dm3pHgUS
# Pyrosm- https://lnkd.in/dr4xR9mt

import warnings

from GeoAutoViz.db_manager import DBManager

from GeoAutoViz.interfaces.DataVisualizer import DataVisualizer


class UrbanFeaturesVisualizer(DataVisualizer):

    def __init__(self, analyzer=None):
        super().__init__()

        warnings.filterwarnings("ignore")

        self.place = analyzer.place

        if analyzer.db_name is None:
            self.db_name = analyzer.place
        else:
            self.db_name = analyzer.db_name

        self.db = DBManager(self.db_name)
        self.local_crs = analyzer.local_crs

        # neighbors wights
        self.queen_1 = None
        self.queen_3 = None

        # merge all datasets
        self.merged = None
        self.percentiles_joined = None
        self.percentiles_standardized = None
        self.urban_types = None

        self.analyzer = analyzer

    def plot_buildings(self):
        self.analyzer.buildings.plot()

    def plot_tessellations(self):
        self.analyzer.tessellations.plot()

    def plot_streets(self):
        self.analyzer.streets.plot()

    def plot_eri(self):
        self.analyzer.buildings.plot("eri", scheme="natural_breaks", legend=True)

    def plot_elongation(self):
        self.analyzer.buildings.plot("elongation", scheme="natural_breaks", legend=True)

    def plot_shared_walls(self):
        self.analyzer.buildings.plot("shared_walls", scheme="natural_breaks", legend=True)

    def plot_neighbor_distance(self):
        self.analyzer.buildings.plot("neighbor_distance", scheme="natural_breaks", legend=True)

    def plot_covered_area(self):
        self.analyzer.tessellations.plot("covered_area", scheme="natural_breaks", legend=True)

    def plot_interbuilding_distance(self):
        self.analyzer.buildings.plot("interbuilding_distance", scheme="natural_breaks", legend=True)

    def plot_adjacency(self):
        self.analyzer.buildings.plot("adjacency", scheme="natural_breaks", legend=True)

    def plot_streets_width(self):
        self.analyzer.streets.plot("width", scheme="natural_breaks", legend=True)

    def plot_streets_width_deviation(self):
        self.analyzer.streets.plot("width_deviation", scheme="natural_breaks", legend=True)

    def plot_streets_openness(self):
        self.analyzer.streets.plot("openness", scheme="natural_breaks", legend=True)

    def plot_tessellations_car(self):
        self.analyzer.tessellations.plot("car", vmin=0, vmax=1, legend=True)

    def plot_nodes_degree(self):
        self.analyzer.streets_nodes.plot("degree", scheme="natural_breaks", legend=True, markersize=1)

    def plot_nodes_closeness(self):
        self.analyzer.streets_nodes.plot("closeness", scheme="natural_breaks", legend=True, markersize=1,
                                 legend_kwds={"fmt": "{:.6f}"})

    def plot_nodes_meshedness(self):
        self.analyzer.streets_nodes.plot("meshedness", legend=True, markersize=1)

    def plot_merged_convexity_50(self):
        self.analyzer.merged.plot(self.analyzer.percentiles_joined, self.merged)

    def plot_urban_types(self):
        self.analyzer.urban_types.plot("cluster", categorical=True, figsize=(8, 8), legend=True)
