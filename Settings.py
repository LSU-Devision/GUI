import json
import Utilities as utils

default_json_path = "config/default_settings.json"
target_json_path = "config/Target-Settings.json"

class SettingsJson():
    def __init__(self, json_file_path=utils.resource_path(default_json_path)):
        ####################################################
        # restructured loading -skylar
        # Load default json
        with open(json_file_path, 'r') as default_json_file:
            self.default_json_data = json.load(default_json_file)

        # Load target json
        with open(utils.resource_path(target_json_path), 'r') as target_json_file:
            self.target_json_data = json.load(target_json_file)

        # Initially load target settings
        self.json_file = self.default_json_data
        self.load_custom_settings()

    ####################################################
    # function to load default json file. -skylar
    def load_default(self):
        with open(utils.resource_path(target_json_path), 'r') as self.json_file:
            self.default_json_data = json.load(self.json_file)
        self.automatic_excel_export = self.default_json_data['automatic excel export']
        self.automatic_prediction_clear_data = self.default_json_data['automatic prediction clear data']
        self.clear_data_on_clear_images = self.default_json_data['clear data on clear images']
        self.save_images_output = self.default_json_data['save images output']

    ####################################################
    # function to load custom settings from json file. -skylar
    def load_custom_settings(self):
        with open(utils.resource_path(default_json_path), 'r') as self.json_file:
            self.default_json_data = self.target_json_data
        self.automatic_excel_export = self.default_json_data['automatic excel export']
        self.automatic_prediction_clear_data = self.default_json_data['automatic prediction clear data']
        self.clear_data_on_clear_images = self.default_json_data['clear data on clear images']
        self.save_images_output = self.default_json_data['save images output']

    ####################################################
    # function to revert back to default settings. -skylar
    def revert_to_default(self):
        # Load default json data
        with open(utils.resource_path(default_json_path), 'r') as self.json_file:
            self.default_json_data = json.load(self.json_file)

        # Overwrite target-settings.json with default data
        with open(utils.resource_path(target_json_path), 'w') as json_file:
            json.dump(self.default_json_data, json_file, indent=4)

        # Load default settings
        self.load_default()
        
    ####################################################
    # updated function to use boolean values -skylar
    def update_json(self, key, value):
        # Load target-settings.json
        with open(utils.resource_path(target_json_path), 'r') as target_json_file:
            self.json_file = json.load(target_json_file)

        # Update data
        self.json_file[key] = value

        # Overwrite all settings in target-settings.json with updated data
        with open(utils.resource_path(target_json_path), 'w') as json_file:
            json.dump(self.json_file, json_file, indent=4)

    ####################################################
    # now returns boolean values instead of strings -skylar
    def get_automatic_excel_export(self):
        return self.automatic_excel_export

    def get_automatic_prediction_clear_data(self):
        return self.automatic_prediction_clear_data

    def get_clear_data_on_clear_images(self):
        return self.clear_data_on_clear_images
    
    def get_save_images_output(self):
        return self.save_images_output
    
    ####################################################
    # each set function uses boolean input and writes as boolean -skylar
    def set_automatic_excel_export(self, value):
        self.automatic_excel_export = value
        self.update_json('automatic excel export', value)

    def set_automatic_prediction_clear_data(self, value):
        self.automatic_prediction_clear_data = value
        self.update_json('automatic prediction clear data', value)

    def set_clear_data_on_clear_images(self, value):
        self.clear_data_on_clear_images = value
        self.update_json('clear data on clear images', value)

    def set_save_images_output(self, value):
        self.save_images_output = value
        self.update_json('save images output', value)