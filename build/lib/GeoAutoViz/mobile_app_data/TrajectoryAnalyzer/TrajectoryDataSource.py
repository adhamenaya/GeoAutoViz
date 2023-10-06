from GeoAutoViz.DatabaseConnector import DatabaseConnector
from GeoAutoViz.interfaces.DataSource import DataSource


class TrajectoryDataSource(DataSource):

    def connect(self):
        db_params = {
            "host": "localhost",
            "database": "mobile_app_data",
            "user": "postgres",
            "password": "root",
        }

        self.db_connector = DatabaseConnector(db_params)
        self.db_connector.connect()

    def disconnect(self):
        pass

    def __init__(self):
        self.db_connector = None
        self.connect()

    def count_users_within_area(self, xmin, ymin, xmax, ymax):
        try:
            with self.db_connector.connection.cursor() as cursor:
                cursor.callproc("count_users_within_area", [xmin, ymin, xmax, ymax])
                result = cursor.fetchone()[0]
                return result
        except Exception as error:
            print(error)
            raise ValueError("Error counting users within the area") from error

    def get_trajectory_points_in_area_with_timestamp(self, xmin, ymin, xmax, ymax):
        try:
            with self.db_connector.connection.cursor() as cursor:
                cursor.callproc("get_trajectory_points_in_area_with_timestamp", [xmin, ymin, xmax, ymax])
                result = cursor.fetchall()
                return result
        except Exception as error:
            print(error)
            raise ValueError("Error getting trajectory points within the area") from error
