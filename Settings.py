import json
default_json = 'settings.json'

class SettingsJson():
    def __init__(self, json_file_path = default_json):
        with open(json_file_path) as json_file_path:
            self.json_file = json.load(json_file_path)
        self.automatic_csv_export = self.json_file['automatic csv export']
        self.automatic_prediction_clear_data = self.json_file['automatic prediction clear data']
        self.clear_data_on_clear_images = self.json_file['clear data on clear images']

