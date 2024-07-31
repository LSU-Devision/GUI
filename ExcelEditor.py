import datetime
import json
import os
import sys
import Utilities as utils
from openpyxl import Workbook, load_workbook
from tkinter import messagebox

# load default settings
default_settings = 'config/excel_settings.json'

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
    load_excel_settings: load the excel settings
    save_excel_settings: save the excel settings
    export_predictions_to_excel: export the predictions to excel
    various getters and setter methods
'''
class ExcelEditor:
    '''
    method: __init__
    description: initialize the class
    '''
    def __init__(self,master=None):
        # set the excel file to none
        self.excel_file = None
        # set the excel label to none
        self.excel_label = None
        # set the excel index value to none
        self.excel_index_value = 'None'
        # set the excel date value to none
        self.excel_date_value = 'None'
        # set the excel time value to none
        self.excel_time_value = 'None'
        # set the excel file name value to none
        self.excel_file_name_value = 'None'
        # set the excel total count value to none
        self.excel_total_count_value = 'None'
        # set the master to the mainframe
        self.master = master
        # load the excel settings
        self.load_excel_settings()

    '''
    method: load_excel_settings
    description: load the excel settings in to the class
    '''
    def load_excel_settings(self):
        # create the self.data variable
        self.data = None
        # open the default settings
        with open(resource_path(default_settings)) as json_file:
            # load the default settings from the json file
            self.data = json.load(json_file)
        # set the excel index value
        self.excel_index_value = self.data['excel_index_column']
        # set the excel date value
        self.excel_date_value = self.data['excel_date_column']
        # set the excel time value
        self.excel_time_value = self.data['excel_time_column']
        # set the excel file name value
        self.excel_file_name_value = self.data['excel_file_name_column']
        # set the excel total count value
        self.excel_total_count_value = self.data['excel_total_count_column']

    '''
    method: save_excel_settings
    description: save the excel settings in to the class
    '''
    def save_excel_settings(self):
        # create the self.data_save variable
        self.data_save = {}
        # set the data save excel index column
        self.data_save['excel_index_column'] = self.excel_index_value
        # set the data save excel date column
        self.data_save['excel_date_column'] = self.excel_date_value
        # set the data save excel time column
        self.data_save['excel_time_column'] = self.excel_time_value
        # set the data save excel file name column
        self.data_save['excel_file_name_column'] = self.excel_file_name_value
        # set the data save excel total count column
        self.data_save['excel_total_count_column'] = self.excel_total_count_value
        # open the default settings
        with open(resource_path(default_settings), 'w') as outfile:
            # dump the data to the json file
            json.dump(self.data_save, outfile,indent=4)

    '''
    method: export_predictions_to_excel
    description: export the predictions to excel
    '''
    def export_predictions_to_excel(self):
        re_order_settings = False
        if self.master.is_data_cleared == False:
            no_cancel = messagebox.askokcancel(title='Data Not Cleared',message='Data has not been cleared since last export. Do you want to continue?',parent=self.master)
            if no_cancel == False:
                return
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
            # set the headers to the first row
            ws.cell(row=1, column=1, value=self.get_excel_headers()[0])
            # append the headers to the worksheet
            for i, header in enumerate(self.get_excel_headers()[1:], start=2):
                # add each header to the appropriate row
                ws.cell(row=1, column=i, value=header)
        # if the index column does exist
        elif has_index_column is True:
            # get the last index value using a for loop
            for cell in ws['A']:
                # update the last index value to the current cel value, traversing down the excel until out of values
                last_index_value = cell.value
        # iterate over the predictions to append to the worksheet
        if does_file_exist is False:
            # get the index of the headers
            index_list = self.get_headers_index()
            # create an empty list for indexing
            edited_prediction_list = []
            # iterate over the predictions
            for prediction in self.master.predictions.predictions_data:
                # clear the prediction list
                edited_prediction_list.clear()
                # iterate over the index values
                for index in index_list:
                    # append the index value from predictions to the list
                    edited_prediction_list.append(prediction[index])
                # append the list to the worksheet
                ws.append(edited_prediction_list)
                # update the internal excel label with the substring
                self.get_substring()
                # update the Mainframe excel label
                self.master.excel_label_title.config(text=self.get_excel_label())


        else:
            possible_headers = ['Index', 'Date', 'Time', 'File Name', 'Total Count']
            # get the headers from the excel file
            excel_header_list = []
            for cell in ws[1]:
                if cell.value in possible_headers:
                    excel_header_list.append(cell.value)
                else:
                    messagebox.showerror("Error", f"Invalid headers in excel file. This is the invalid header {cell.value}")
                    return
            if len(excel_header_list) > 5:
                messagebox.showerror("Error", "Headers in excel file are greater than 5. This is not supported.")
                return
            if len(excel_header_list) != len(set(excel_header_list)):
                messagebox.showerror("Error", "Headers in excel file are not unique. This is not supported.")
                return
            order_check = True
            current_header_list = self.get_excel_headers()
            index = 0
            for header in excel_header_list:
                if header != current_header_list[index]:
                    order_check = False
                    break
                else:
                    order_check = True
                index += 1
            if order_check is False:
                re_order_settings = messagebox.askyesno("Notice", "Headers in excel file are not in the correct order. Would you like to reorder the settings to match the order in the excel file?")
                excel_header_index = self.get_headers_index(excel_header_list)
                edited_excel_prediction_list = []
                for prediction in self.master.predictions.predictions_data:
                    edited_excel_prediction_list.clear()
                    for index in excel_header_index:
                        edited_excel_prediction_list.append(prediction[index])
                    ws.append(edited_excel_prediction_list)
            else:
                for prediction in self.master.predictions.predictions_data:
                    # create a list for data manipulation, tuple's are immutable (not changable)
                    prediction_list = list(prediction)
                    # update the index values to reflect the values on the sheet
                    prediction_list[0] = prediction_list[0] = prediction_list[0] + last_index_value
                    # append the list to the worksheet
                    ws.append(prediction_list)
            if re_order_settings is True:
                header_dict = {}
                for header in possible_headers:
                    try:
                        header_dict[header] = excel_header_list.index(header)
                    except ValueError:
                        header_dict[header] = 'None'
                self.excel_index_value = header_dict['Index']
                self.excel_date_value = header_dict['Date']
                self.excel_time_value = header_dict['Time']
                self.excel_file_name_value = header_dict['File Name']
                self.excel_total_count_value = header_dict['Total Count']
                self.save_excel_settings()
        # try statement to save the workbook
        try:
            # save the workbook
            wb.save(self.get_excel_file())
            # show success
            messagebox.showinfo("Success", "Successfully exported predictions to excel")
        # if the file is read only
        except PermissionError:
            # show an error
            messagebox.showerror("Permissions Error", "Excel file may be open, or you may have Read only attributes, please close the excel file or check permissions")
            # exit the method
            return
        # boolean check for clearing variables
        self.master.is_data_cleared = False
        # boolean check for automatic prediction clearing
        if self.master.settings.get_automatic_prediction_clear_data():
            # clear the predictions
            self.master.predictions.predictions_data.clear()
            # set the boolean check to True
            self.master.is_data_cleared = True
        return re_order_settings


    def get_excel_index_column_index(self):
        return self.excel_index_value
    def get_excel_date_column_index(self):
        return self.excel_date_value
    def get_excel_time_column_index(self):
        return self.excel_time_value
    def get_excel_file_name_column_index(self):
        return self.excel_file_name_value
    def get_excel_total_count_column_index(self):
        return self.excel_total_count_value
    def get_substring(self):
        self.excel_label = utils.string_to_substring(self.excel_file)
    def get_excel_file(self):
        return self.excel_file
    def get_excel_label(self):
        return self.excel_label
    def set_excel_file(self, excel_file):
        self.excel_file = excel_file
    def set_excel_label(self, excel_label):
        self.excel_label = excel_label
    def set_excel_index_column_value(self, excel_index):
        self.excel_index_value = excel_index
    def set_excel_date_column_value(self, excel_date):
        self.excel_date_value = excel_date
    def set_excel_time_column_value(self, excel_time):
        self.excel_time_value = excel_time
    def set_excel_file_name_column_value(self, excel_file_name):
        self.excel_file_name_value = excel_file_name
    def set_excel_total_count_column_value(self, excel_total_count):
        self.excel_total_count_value = excel_total_count

    '''
    method: get_excel_headers
    description: get and order the excel headers according to the settings
    '''
    def get_excel_headers(self):
        # create a list of the header values
        value_list = [
            self.excel_index_value,
            self.excel_date_value,
            self.excel_time_value,
            self.excel_file_name_value,
            self.excel_total_count_value
        ]
        # create a new list to store the values
        new_list = []
        # iterate over the values in the header list
        for value in value_list:
            # if the value is not None, append it to the new list
            if value != 'None':
                # append the value
                new_list.append(value)
        # sort the new list by numerical value
        new_list.sort()
        # create a new list to store the index values of the header list
        index_list = []
        # iterate over the new list and store the index values in the index list
        for index in new_list:
            # append the index value
            index_list.append(value_list.index(index))
        # create a list for the headers
        headers_list = []
        # iterate over the index list
        for index in index_list:
            # if the index is for the Index
            if index == 0:
                # append the index to the headers list
                headers_list.append('Index')
                # if the index is for the Date
            elif index == 1:
                # append the date to the headers list
                headers_list.append('Date')
            # if the index is for the Time
            elif index == 2:
                # append the time to the headers list
                headers_list.append('Time')
            # if the index is for the File Name
            elif index == 3:
                # append the file name to the headers list
                headers_list.append('File Name')
            # if the index is for the Total Count
            elif index == 4:
                # append the total count to the headers list
                headers_list.append('Total Count')
        # return the headers list
        return headers_list
    '''
    method: get_headers_index
    description: get the index values of the headers
    '''
    def get_headers_index(self,header_list=None):
        # create a list for the index values
        index_list = []
        # get the header list
        if header_list is None:
            header_list = self.get_excel_headers()
        # iterate over the header list
        for header in header_list:
            # if the header is Index
            if header == 'Index':
                # append the index to the index list
                index_list.append(0)
            # if the header is Date
            elif header == 'Date':
                # append the date to the index list
                index_list.append(1)
            # if the header is Time
            elif header == 'Time':
                # append the time to the index list
                index_list.append(2)
            # if the header is File Name
            elif header == 'File Name':
                # append the file name to the index list
                index_list.append(3)
            # if the header is Total Count
            elif header == 'Total Count':
                # append the total count to the index list
                index_list.append(4)
        # return the index list
        return index_list