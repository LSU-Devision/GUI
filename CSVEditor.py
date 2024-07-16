import csv
import Utilities as utils
class CSVEditor:
    def __init__(self):
        self.csv_file = None
        self.csv_label = None


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