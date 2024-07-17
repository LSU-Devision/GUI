import csv
import Utilities as utils
import json

default_settings = 'csv_settings.json'
class CSVEditor:
    def __init__(self):
        self.csv_file = None
        self.csv_label = None
        self.csv_index_value = 'None'
        self.csv_date_value = 'None'
        self.csv_time_value = 'None'
        self.csv_file_name_value = 'None'
        self.csv_total_count_value = 'None'
        self.load_csv_settings()

    def load_csv_settings(self):
        self.data = None
        with open(default_settings) as json_file:
            self.data = json.load(json_file)
        self.csv_index_value = self.data['csv_index_column']
        self.csv_date_value = self.data['csv_date_column']
        self.csv_time_value = self.data['csv_time_column']
        self.csv_file_name_value = self.data['csv_file_name_column']
        self.csv_total_count_value = self.data['csv_total_count_column']

    def save_csv_settings(self):
        self.data_save = {}
        self.data_save['csv_index_column'] = self.csv_index_value
        print(self.data_save['csv_index_column'] + "  test  " + self.csv_index_value)
        self.data_save['csv_date_column'] = self.csv_date_value
        self.data_save['csv_time_column'] = self.csv_time_value
        self.data_save['csv_file_name_column'] = self.csv_file_name_value
        self.data_save['csv_total_count_column'] = self.csv_total_count_value
        with open(default_settings, 'w') as outfile:
            json.dump(self.data_save, outfile,indent=4)
    def get_csv_index_column_index(self):
        return self.csv_index_value

    def get_csv_date_column_index(self):
        return self.csv_date_value
    def get_csv_time_column_index(self):
        return self.csv_time_value
    def get_csv_file_name_column_index(self):
        return self.csv_file_name_value
    def get_csv_total_count_column_index(self):
        return self.csv_total_count_value
    def get_substring(self):
        self.csv_label = utils.string_to_substring(self.csv_file)
    def get_csv_file(self):
        return self.csv_file
    def get_csv_label(self):
        return self.csv_label
    def set_csv_file(self, csv_file):
        self.csv_file = csv_file
    def set_csv_label(self, csv_label):
        self.csv_label = csv_label
    def set_csv_index_column_value(self, csv_index):
        self.csv_index_value = csv_index
        print(self.csv_index_value)
    def set_csv_date_column_value(self, csv_date):
        self.csv_date_value = csv_date
    def set_csv_time_column_value(self, csv_time):
        self.csv_time_value = csv_time
    def set_csv_file_name_column_value(self, csv_file_name):
        self.csv_file_name_value = csv_file_name
    def set_csv_total_count_column_value(self, csv_total_count):
        self.csv_total_count_value = csv_total_count