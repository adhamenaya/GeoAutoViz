import json


class DataProcessor:
    def __init__(self, data_source, data_analyzer, data_visualizer):
        self.data_source = data_source
        self.data_analyzer = data_analyzer
        self.data_visualizer = data_visualizer

    def load_configuration(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            analysis_plugins = config.get('analysis_plugins', [])
        return analysis_plugins

    def process_data(self):
        data = self.data_source.read_data()
        results = self.data_analyzer.analyze(data)
        self.data_visualizer.visualize(results)
