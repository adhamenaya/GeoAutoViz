from GeoAutoViz.DatabaseConnector import DatabaseConnector
from GeoAutoViz.interfaces.DataSource import DataSource


class UKZonesDataSource(DataSource):

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

    def get_mosa_in_area(self, xmin, ymin, xmax, ymax):
        try:
            with self.db_connector.connection.cursor() as cursor:
                cursor.callproc("get_mosa_in_area", [xmin, ymin, xmax, ymax])
                result = cursor.fetchall()
                return result
        except Exception as error:
            print(error)
            raise ValueError("Error in get_mosa_in_area") from error
