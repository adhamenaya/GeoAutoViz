from GeoAutoViz.interfaces.DataSource import DataSource


class PostGISDataSource(DataSource):
    def __init__(self, place, db_name=None, local_crs=5514):
        super().__init__()
        # Initialize PostGIS-specific attributes here

    def extract_data(self):
        # Implement the extraction logic for PostGIS
        pass
