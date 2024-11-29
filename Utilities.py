import os
import json
import sys
from tktooltip import ToolTip
from tkinter import messagebox
'''
Contributors: Alex Mensen-Johnson, Skylar Wilson, Sunella Ramnath
Class: Utilities
Description: Utility functions
Params:
    None
Methods:
    string_to_substring(string)
    boolean_text_conversion(boolean)
'''

FROG_EGG_COUNTER_BASE_PATH = os.path.basename('models/frog-egg-counter')
OYSTER_SEED_COUNTER_BASE_PATH = os.path.basename('models/Oyster_model')
XENOPUS_FROG_EMBRYO_BASE_PATH = os.path.basename('models/Xenopus Frog Embryos Classification Model')
def string_to_substring(string):
    """
    Method: string_to_substring
    Description: returns the last 20 characters of a string
    :param string:
    :return: returns the sub string of the sting passed in
    """
    substring = string[-20:]
    return substring

def resource_path(relative_path):
    """
    Method: resource_path
    Description: Get absolute path to resource, works for dev and for PyInstaller
    :param relative_path:
    :return: returns the absolute path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def boolean_text_conversion(boolean):
    """
    Method: boolean_text_conversion
    Description: returns the text representation of a boolean
    :param boolean:
    :return: Off or On depending on the boolean value
    """
    if boolean == True:
        return 'On'
    elif boolean == False:
        return 'Off'
    else:
        raise ValueError('Error: Invalid boolean value')

def string_to_boolean(string):
    """
    Method: string_to_boolean
    Description: returns the boolean representation of a string
    :param string:
    :return: returns the boolean value based off of the string passed in
    """
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        raise ValueError('Error: Invalid boolean string')
    
def check_file_extension(file_name, file_type):

    file_name_split = file_name.split('.')
    excel_types = ['xlsx', 'xls', 'csv']
    image_types = ['tif', 'tiff', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'npy', 'npz', 'heic']
    message_title = 'Incompatible File Type Warning'
    message_start = f'selected file is not a '
    message_end = f'\n Would you like to remove the file and continue?\n Select no to abort the action\n your file type is {file_name_split[-1]}'

    if file_type == 'excel':
        if file_name_split[-1].lower() not in excel_types:
            user_answer = messagebox.showerror(message_title,  message_start + f''.join([ str('.' + excel_type + ', ') for excel_type in excel_types]))
            return False
    elif file_type == 'image':
        if file_name_split[-1].lower() not in image_types:
            user_answer = messagebox.askyesno(message_title,  message_start + f''.join([ str('.' + image_type + ', ') for image_type in image_types]) + message_end)
            return user_answer
    
    return None



class ToolTips():
    """
    Class: ToolTips
    Description: Tool tip class, tool tips will be displayed when the mouse hovers over the buttons
    Params:
        None
    Methods:
        __init__(self,buttons,frame,delay=0.5)
        get_mainframe_data(self)
        get_excel_window_data(self)
        get_settings_data(self)
    """
    def __init__(self,buttons,frame,delay=0.5):
        """
        method: init
        description: initialize the class
        :param buttons: list of buttons to display tool tips
        :param frame: the frame designated for the tool tips
        :param delay: the delay time before displaying the tool tip, default is half a second
        """
        # creates a variable for the buttons locally
        self.buttons=buttons
        # creates a variable for the delay locally
        self.delay=delay
        # loads the json file
        with open(resource_path('config/tool-tip.json'), 'r') as file:
            # loads the json file
            self.data =json.load(file)
        # checks if the frame is the main frame
        if frame == 'main_frame':
            # loads the data from the main frame section of the JSON file
            self.data = self.data['main_frame']
        # checks if the frame is the excel window
        elif frame == 'excel_window':
            # loads the data from the excel window section of the JSON file
            self.data = self.data['excel_window']
        # checks if the frame is the settings
        elif frame == 'settings':
            # loads the data from the settings section of the JSON file
            self.data = self.data['settings']
        # checks if the frame is invalid
        else:
            # raises an error
            raise ValueError('Error: Invalid frame')
        # creates a tool tip for each button assigned
        for key in self.buttons:
            ToolTip(self.buttons[key], self.data[key], self.delay)



    def get_mainframe_data(self):
        return self.data['main_frame']

    def get_excel_window_data(self):
        return self.data['excel_window']

    def get_settings_data(self):
        return self.data['settings']

class StringChecker():
    """
    Class: StringChecker
    Description: String checker class
    Params:
        None
    Methods:
        filename_checker(self, filename)
        get_invalid_characters(self)
        get_reserved_filenames(self)
        get_files_cannot_end_with(self)
    """
    def __init__(self):
        """
        method: initialization method
        description: creates key variables for use in class methods
        self.invalid_characters = list of invalid characters
        self.invalid_filenames = list of reserved filenames
        self.files_cannot_end_with = list of files that cannot end with a period
        """
        self.invalid_characters = ['\\', '/', ':', ';', '?', '*', '<', '>', '|', '"', '.']
        self.invalid_filenames = ['CON', 'PRN', 'AUX', 'NUL', 'COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT0', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9','NONE']
        self.files_cannot_end_with = ['.', ' ']
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.acceptable_folder_characters = [' ', '-', '_']

    def filename_checker(self, filename):
        """
        method: filename checker
        description: checks if filename is valid
        :param filename: name to be checked for validity
        :return: boolean value true or false based of the validity of the filename, False if valid, True if invalid
        """
        # create a boolean variable named flag
        flag = False
        # check if filename is empty
        if filename == '':
            # set flag to true
            flag = True
            # return flag
            return flag
        # check if filename contains invalid characters
        for breaker in self.invalid_characters:
            # if the filename contains an invalid character
            if breaker in filename:
                # set flag to true
                flag = True
                # return flag
                return flag
        # check if filename is reserved
        for name in self.invalid_filenames:
            # if the filename is reserved
            if name == filename.upper():
                # set flag to true
                flag = True
                # return flag
                return flag
        # check if filename cannot end with a period
        for ending in self.files_cannot_end_with:
            # if the filename cannot end with a period
            if filename.endswith(ending):
                # set flag to true
                flag = True
                # return flag
                return flag
        # return flag
        return flag

    def folder_checker(self,folder_name):
        # create a boolean variable named flag
        flag = False
        # check if folder name is empty
        if folder_name == '':
            flag = True
            return flag
        # Create valid characters list
        valid_characters = self.acceptable_folder_characters + self.alphabet + self.numbers
        for character in folder_name:
            if character.upper() not in valid_characters:
                flag = True
                return flag
        if len(folder_name) > 30:
            flag = True
            return flag
        if folder_name.startswith(' ') or folder_name.endswith(' '):
            flag = True
            return flag
        return flag



    def get_invalid_characters(self):
        return self.invalid_characters

    def get_reserved_filenames(self):
        return self.invalid_filenames

    def get_files_cannot_end_with(self):
        return self.files_cannot_end_with

    def get_invalid_characters_string(self):
        """
        method: get invalid characters string
        description: returns a string of the invalid characters
        :return: returns a string of invalid characters
        """
        string_builder = ''
        for each in self.invalid_characters:
            string_builder = f'{string_builder} {each}'
        return string_builder

    def get_reserved_filenames_string(self):
        """
        method: get reserved filenames string
        description: returns a string of the reserved filenames
        :return: returns a string of the reserved filenames
        """
        string_builder = ''
        for each in self.invalid_filenames:
            string_builder = f'{string_builder} {each}'
        return string_builder

    def get_files_cannot_end_with_string(self):
        """
        method: get files cannot end with string
        description: returns a string of the files that cannot end with a period
        :return: returns a string of the two things a file cannot end with, a period and a space
        """
        string_builder = ''
        for each in self.files_cannot_end_with:
            string_builder = f'{string_builder} {each}'
        return string_builder

def model_path_to_name(path):
    if os.path.basename(path) == FROG_EGG_COUNTER_BASE_PATH:
        return 'Frog Egg Counter'
    elif os.path.basename(path) == OYSTER_SEED_COUNTER_BASE_PATH:
        return ' Oyster Seed Counter'
    elif os.path.basename(path) == XENOPUS_FROG_EMBRYO_BASE_PATH:
        return 'Frog Egg Classification'
    elif os.path.exists(path):
        return 'User Model'
    else:
        return 'None'

def is_excel_file(file_path):
    extensions = ['.xlsx', '.xls', '.xltx', '.xltm','.xml', '.csv','.xlsm']
    return any(file_path.lower().endswith(ext) for ext in extensions)