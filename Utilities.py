import os

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

