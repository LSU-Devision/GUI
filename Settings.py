import json
default_json = 'default_settings.json'

class SettingsJson():
    def __init__(self, json_file_path = default_json):
        with open(json_file_path) as json_file_path:
            self.json_file = json.load(json_file_path)
        self.json_file_path = self.json_file['current settings']
        with open(self.json_file_path) as json_file:
            self.json_file = json.load(json_file)
        self.automatic_csv_export = self.json_file['automatic csv export']
        self.automatic_prediction_clear_data = self.json_file['automatic prediction clear data']
        self.clear_data_on_clear_images = self.json_file['clear data on clear images']
        # added for save images toggle -skylar
        self.save_images_output = self.json_file['save images output']


    def update_json(self):
        self.json_file['automatic csv export'] = self.automatic_csv_export
        self.json_file['automatic prediction clear data'] = self.automatic_prediction_clear_data
        self.json_file['clear data on clear images'] = self.clear_data_on_clear_images
        # added for save images toggle -skylar
        self.json_file['save images output'] = self.save_images_output
        with open(default_json, 'w') as json_file:
            json.dump(self.json_file, json_file, indent=4)


    def get_automatic_csv_export(self):
        return self.automatic_csv_export

    def get_automatic_prediction_clear_data(self):
        return self.automatic_prediction_clear_data

    def get_clear_data_on_clear_images(self):
        return self.clear_data_on_clear_images
    
    # added for save images toggle -skylar
    def get_save_images_output(self):
        return self.save_images_output

    def set_automatic_csv_export(self, value):
        self.automatic_csv_export = value
        self.update_json()

    def set_automatic_prediction_clear_data(self, value):
        self.automatic_prediction_clear_data = value
        self.update_json()

    def set_clear_data_on_clear_images(self, value):
        self.clear_data_on_clear_images = value
        self.update_json()

    # added for save images toggle -skylar
    def set_save_images_output(self, value):
        self.save_images_output = value
        self.update_json()