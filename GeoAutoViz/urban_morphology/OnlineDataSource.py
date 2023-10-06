import osmnx

from GeoAutoViz.interfaces.DataSource import DataSource

class OnlineDataSource(DataSource):
    def __init__(self, place, data_type):
        self.place = place
        self.data_type = data_type  # Specify 'buildings', 'tessellations', or 'streets'

    def extract_data(self):
        print(f"Extracting {self.data_type} online...")
        if self.data_type == 'buildings':
            return osmnx.geometries.geometries_from_place(self.place, tags={'building': True})
        elif self.data_type == 'tessellations':
            # Implement tessellation extraction logic
            pass
        elif self.data_type == 'streets':
            # Implement streets extraction logic
            pass
