import json
import Utilities as utils

default_json_path = "config/default_settings.json"

class SettingsJson():
    """
    :class:`SettingsJson`
    :description: Class for the SettingsJson to manage settings for the mainframe
    authors: Alex Mensen-Johnson, Skylar Wilson
    :param: json_file_path = path to the json file
    :method: load_default
    :method: revert_to_default
    :method: get_automatic_excel_export
    :method: get_automatic_prediction_clear_data
    :method: get_clear_data_on_clear_images
    :method: get_save_images_output
    """
    def __init__(self, json_file_path=utils.resource_path(default_json_path)):
        """
        :method: init
        :param json_file_path:
        """
        with open(json_file_path, 'r') as default_json_file:
            self.default_json_data = json.load(default_json_file)
        self.json_file = self.default_json_data
        self.runtime_json_data = self.default_json_data['runtime settings']
        self.saved_files_json_data = self.default_json_data['saved files']
        self.load_default()


    def load_default(self):
        """
        :method: load_default
        :description: Loads the default settings
        :return: nothing
        """
        self.automatic_excel_export = self.runtime_json_data['automatic excel export']
        self.automatic_prediction_clear_data = self.runtime_json_data['automatic prediction clear data']
        self.clear_data_on_clear_images = self.runtime_json_data['clear data on clear images']
        self.save_images_output = self.runtime_json_data['save images output']


    def revert_to_default(self):
        """
        :method: revert_to_default
        :description: Reverts all settings to default
        :return:
        """
        self.automatic_excel_export = False
        self.automatic_prediction_clear_data = False
        self.clear_data_on_clear_images = True
        self.save_images_output = False
        self.runtime_json_data['automatic excel export'] = self.automatic_excel_export
        self.runtime_json_data['automatic prediction clear data'] = self.automatic_prediction_clear_data
        self.runtime_json_data['clear data on clear images'] = self.clear_data_on_clear_images
        self.runtime_json_data['save images output'] = self.save_images_output
        self.default_json_data['runtime settings'] = self.runtime_json_data

        with open(utils.resource_path(default_json_path), 'w') as json_file:
            json.dump(self.default_json_data, json_file, indent=4)

        self.load_default()
        

    def update_json(self, key, value,section='runtime settings'):
        """
        :method: update_json
        :description: Updates the json file with new settings
        :param key: key setting to update
        :param value: the new value of the setting
        :return: nothing
        """

        # Update data
        self.runtime_json_data[key] = value
        if section == 'runtime settings':
            self.runtime_json_data[key] = value
            self.default_json_data['runtime settings'] = self.runtime_json_data
        elif section == 'saved files':
            self.saved_files_json_data[key] = value
            self.default_json_data['saved files'] = self.saved_files_json_data

        # Overwrite all settings in default-settings.json with updated data
        with open(utils.resource_path(default_json_path), 'w') as json_file:
            json.dump(self.default_json_data, json_file, indent=4)

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
        self.update_json('automatic excel export', value, 'runtime settings')

    def set_automatic_prediction_clear_data(self, value):
        self.automatic_prediction_clear_data = value
        self.update_json('automatic prediction clear data', value, 'runtime settings')

    def set_clear_data_on_clear_images(self, value):
        self.clear_data_on_clear_images = value
        self.update_json('clear data on clear images', value, 'runtime settings')

    def set_save_images_output(self, value):
        self.save_images_output = value
        self.update_json('save images output', value, 'runtime settings')