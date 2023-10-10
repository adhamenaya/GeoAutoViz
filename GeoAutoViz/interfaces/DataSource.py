from abc import abstractmethod


class Offline:
    DB = 1
    CSV = 2
    JSON = 3

class Mode:
    Offline = 1
    Online = 2



class DataSource:
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
