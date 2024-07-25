import datetime
import json
import os
import sys
import Utilities as utils
from openpyxl import Workbook, load_workbook
from tkinter import messagebox

# load default settings
default_settings = 'config/csv_settings.json'

def resource_path(relative_path):
    """ Get absolute path to resource, needed for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

'''
Class: ExcelEditor
Contributors: Alex Mensen-Johnson, Skylar Wilson
Description: Class for the Excel Editor to manage excel files for the mainframe
Params:
    master = master class aka MainFrame
methods:
    __init__: initialize the class
    load_csv_settings: load the csv settings
    save_csv_settings: save the csv settings
    export_predictions_to_csv: export the predictions to csv
    various getters and setter methods
'''
class ExcelEditor:
    '''
    method: __init__
    description: initialize the class
    '''
    def __init__(self,master=None):
        # set the csv file to none
        self.csv_file = None
        # set the csv label to none
        self.csv_label = None
        # set the csv index value to none
        self.csv_index_value = 'None'
        # set the csv date value to none
        self.csv_date_value = 'None'
        # set the csv time value to none
        self.csv_time_value = 'None'
        # set the csv file name value to none
        self.csv_file_name_value = 'None'
        # set the csv total count value to none
        self.csv_total_count_value = 'None'
        # set the master to the mainframe
        self.master = master
        # load the csv settings
        self.load_csv_settings()

    '''
    method: load_csv_settings
    description: load the csv settings in to the class
    '''
    def load_csv_settings(self):
        # create the self.data variable
        self.data = None
        # open the default settings
        with open(resource_path(default_settings)) as json_file:
            # load the default settings from the json file
            self.data = json.load(json_file)
        # set the csv index value
        self.csv_index_value = self.data['csv_index_column']
        # set the csv date value
        self.csv_date_value = self.data['csv_date_column']
        # set the csv time value
        self.csv_time_value = self.data['csv_time_column']
        # set the csv file name value
        self.csv_file_name_value = self.data['csv_file_name_column']
        # set the csv total count value
        self.csv_total_count_value = self.data['csv_total_count_column']

    '''
    method: save_csv_settings
    description: save the csv settings in to the class
    '''
    def save_csv_settings(self):
        # create the self.data_save variable
        self.data_save = {}
        # set the data save csv index column
        self.data_save['csv_index_column'] = self.csv_index_value
        # set the data save csv date column
        self.data_save['csv_date_column'] = self.csv_date_value
        # set the data save csv time column
        self.data_save['csv_time_column'] = self.csv_time_value
        # set the data save csv file name column
        self.data_save['csv_file_name_column'] = self.csv_file_name_value
        # set the data save csv total count column
        self.data_save['csv_total_count_column'] = self.csv_total_count_value
        # open the default settings
        with open(resource_path(default_settings), 'w') as outfile:
            # dump the data to the json file
            json.dump(self.data_save, outfile,indent=4)

    '''
    method: export_predictions_to_csv
    description: export the predictions to csv
    '''
    def export_predictions_to_csv(self):
        # set the current time with a format
        current_time = datetime.datetime.now().strftime("%m-%d-%Y_%I-%M-%S %p")
        # check to see if the excel file exists
        if self.get_excel_file() is None:
            # set the excel file with the specified name
            self.set_excel_file(os.path.join('output', f'predictions_{current_time}.xlsx'))
        # check to see if the output folder exists
        if not os.path.exists('output'):
            # create the output folder
            os.makedirs('output')
        # create boolean variable to check if the file exists
        does_file_exist = True
        # try to create the workbook
        try:
            # load the workbook
            wb = load_workbook(self.get_excel_file())
            # set the worksheet
            ws = wb.active
        # if the file does not exist
        except FileNotFoundError:
            # create the workbook
            wb = Workbook()
            # set the worksheet
            ws = wb.active
            # set the boolean variable to false
            does_file_exist = False
        # create a boolean variable to check if the index column exists
        has_index_column = 'Index' in [cell.value for cell in ws['A']]
        # set a value for the last index value
        last_index_value = 0
        # if the file does not exist
        if does_file_exist is False:
            # create the headers
            headers = ['Index', 'Date', 'Time', 'File Name', ' Total Count']
            # append the headers to the worksheet
            ws.append(headers)
        # if the index column does exist
        elif has_index_column is True:
            # get the last index value using a for loop
            for cell in ws['A']:
                # update the last index value to the current cel value, traversing down the excel until out of values
                last_index_value = cell.value
        # iterate over the predictions to append to the worksheet
        for prediction in self.master.predictions.predictions_data:
            # create a list for data manipulation, tuple's are immutable (not changable)
            prediction_list = list(prediction)
            # update the index values to reflect the values on the sheet
            prediction_list[0] = prediction_list[0] + last_index_value
            # append the list to the worksheet
            ws.append(prediction_list)
        # try statement to save the workbook
        try:
            # save the workbook
            wb.save(self.get_excel_file())
        # if the file is read only
        except PermissionError:
            # show an error
            messagebox.showerror("Permissions Error", "Excel file may have Read only attribute, please check permissions")
        # boolean check for clearing variables
        if self.master.settings.get_automatic_prediction_clear_data():
            # clear the predictions
            self.master.predictions.predictions_data.clear()

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
    def get_excel_file(self):
        return self.csv_file
    def get_csv_label(self):
        return self.csv_label
    def set_excel_file(self, csv_file):
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