class UrbanFeaturesDataSource:
    def __init__(self, data_source, place, db_name=None, local_crs=5514):
        super().__init__()
        self.data_source = data_source
        # Other attributes

    def extract_data(self):
        data = self.data_source.extract_data()
        # Other processing logic
