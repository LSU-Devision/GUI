import os
import json
import sys
from tktooltip import ToolTip
'''
Creator: Alex Mensen-Johnson
Contributors:
Class: Utilities
Description: Utility functions
Params:
    None
Methods:
    string_to_substring(string)
    boolean_text_conversion(boolean)
'''
def string_to_substring(string):
    substring = string[-20:]
    return substring

def resource_path(relative_path):
    """ Get absolute path to resource, needed for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def boolean_text_conversion(boolean):
    if boolean == True:
        return 'On'
    elif boolean == False:
        return 'Off'
    else:
        raise ValueError('Error: Invalid boolean value')

def string_to_boolean(string):
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        raise ValueError('Error: Invalid boolean string')

class ToolTips():
    def __init__(self,buttons,frame,delay=0.5):
        self.buttons=buttons
        self.delay=delay
        with open(resource_path('config/tool-tip.json'), 'r') as file:
            self.data =json.load(file)
        if frame == 'main_frame':
            self.data = self.data['main_frame']
        elif frame == 'excel_window':
            self.data = self.data['excel_window']
        elif frame == 'settings':
            self.data = self.data['settings']
        else:
            raise ValueError('Error: Invalid frame')

        for key in self.buttons:
            ToolTip(self.buttons[key], self.data[key], self.delay)



    def get_mainframe_data(self):
        return self.data['main_frame']

    def get_excel_window_data(self):
        return self.data['excel_window']

    def get_settings_data(self):
        return self.data['settings']

