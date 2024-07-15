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
    else:
        return 'Off'

