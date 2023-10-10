from GeoAutoViz.mobile_app_data.TrajectoryAnalyzer.TrajectoryDataSource import TrajectoryDataSource


class TrajectoryAnalyzer:
    def __init__(self):
        self.ds = TrajectoryDataSource()

    def count_users_within_area(self, xmin, ymin, xmax, ymax):
        self.ds.count_users_within_area(xmin, ymin, xmax, ymax)
