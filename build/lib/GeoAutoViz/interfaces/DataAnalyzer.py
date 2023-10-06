from abc import ABC, abstractmethod


class DataAnalyzer(ABC):
    @abstractmethod
    def analyze_data(self):
        pass
