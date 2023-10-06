import psycopg2


class DatabaseConnector:
    def __init__(self, db_params):
        self.db_params = db_params
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("Connected to DB")
        except Exception as error:
            raise ConnectionError("Could not connect to the database") from error

    def disconnect(self):
        if self.connection:
            self.connection.close()
