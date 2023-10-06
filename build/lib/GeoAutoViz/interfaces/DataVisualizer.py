from abc import ABC, abstractmethod


class DataVisualizer(ABC):
    @abstractmethod
    def visualize_data(self):
        pass
