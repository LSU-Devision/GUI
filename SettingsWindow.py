import tkinter as tk
from tkinter import ttk
import Utilities as utils

'''
Class SettingsWindow
Contributors: Skylar Wilson, Alex Mensen-Johnson, Sunella Ramnath
Class: Settings Window
Description: Settings Window for the main frame
Methods:
init
create_page
load_page
toggle_automatic_excel
toggle_automatic_prediction_data_clear
toggle_clear_data_on_clear_images
toggle_save_images
reset_settings
'''
class SettingsWindow(tk.Toplevel):
    '''
    initialization method
    creates class variables for the settings window
    parameters:
    master: the mainframe window
    container: the App window
    settings: the settings object
    '''
    def __init__(self, master=None,container=None,settings=None):
        # creates class variables for the settings window
        super().__init__(master=master)
        # creates a class variable for the App window
        self.container = container
        # creates a class variable for the settings object
        self.settings = settings
        # variable for the width of the main window
        main_window_width = self.container.winfo_width()
        # variable for the height of the main window
        main_window_height = self.container.winfo_height()
        # variables for the pop up window width
        pop_up_window_width = 300
        # variables for the pop up window height
        pop_up_window_height = 400
        # set the position of the pop up window
        x = main_window_width + 75
        # set the position of the pop up window
        y = main_window_height // 2 - pop_up_window_height // 2  # center the pop-up window vertically
        # set the title of the pop up window
        self.title('Settings')
        # set the geometry of the pop up window
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        # convert frame into notebook
        self.notebook = ttk.Notebook(self)
        # add the notebook using the grid method
        self.notebook.grid(row=0, column=0)
        # create the first tab
        self.tab1 = ttk.Frame(self.notebook)
        # create the second tab
        self.tab2 = ttk.Frame(self.notebook)
        # add the Basic tab
        self.notebook.add(self.tab1, text="Basic", )
        # add the Advanced tab
        self.notebook.add(self.tab2, text="Advanced")
        # run the settings page
        self.run()


        '''
        method: create page
        creates the buttons and labels for the settings page and assigns the relative function
        '''
    def create_page(self):
        # create the automatic excel export label
        self.automatic_excel_export_label = ttk.Label(self.tab1, text=utils.boolean_text_conversion(self.settings.get_automatic_excel_export()), font=50)
        # create the automatic excel export button
        self.automatic_excel_export = ttk.Button(self.tab1, text='Automatic Export To Excel', command= lambda : self.toggle_label('self.settings.automatic_excel_export',self.automatic_excel_export_label))
        # create the automatic prediction data clear label
        self.automatic_prediction_data_clear_label = ttk.Label(self.tab1,text=utils.boolean_text_conversion(self.settings.get_automatic_prediction_clear_data()),font=50)
        # create the automatic prediction data clear button
        self.automatic_prediction_data_clear = ttk.Button(self.tab1,text='Automatic Clear Data On Predict',command= lambda : self.toggle_label('self.settings.automatic_prediction_clear_data',self.automatic_prediction_data_clear_label))
        # create the clear data on clear images label
        self.clear_data_on_clear_images_label = ttk.Label(self.tab1, text=utils.boolean_text_conversion(self.settings.get_clear_data_on_clear_images()), font=50)
        # create the clear data on clear images button
        self.clear_data_on_clear_images_button = ttk.Button(self.tab1, text='Clear Data When Clearing Images',command=lambda  : self.toggle_label('self.settings.clear_data_on_clear_images',self.clear_data_on_clear_images_label))
        # create the save images output label
        self.save_images_output_label = ttk.Label(self.tab1, text=utils.boolean_text_conversion(self.settings.get_save_images_output()), font=50)
        # create the save images output button
        self.save_images_output_button = ttk.Button(self.tab1, text='Save Images To Output',command= lambda : self.toggle_label('self.settings.save_images_output',self.save_images_output_label))
        # create the reset settings button
        self.default_settings_button = ttk.Button(self.tab1, text='Reset To Default Settings',command=self.reset_settings)
        # future button to eliminate duplicate windows
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())


    def button_dict(self):
        return {
            'automatic_export_to_excel': self.automatic_excel_export,
            'automatic_clear_data_on_predict': self.automatic_prediction_data_clear,
            'clear_data_when_clearing_images': self.clear_data_on_clear_images_button,
            'save_images_to_output': self.save_images_output_button,
            'reset_to_default_settings': self.default_settings_button
        }
    '''
    method: load page
    creates the buttons and labels for the settings page and assigns the relative function
    '''
    def load_page(self):
        # sets the automatic excel export button to the grid
        self.automatic_excel_export.grid(row=0, column=0, pady=15, padx=15)
        # sets the automatic excel export label to the grid
        self.automatic_excel_export_label.grid(row=0, column=1, pady=15, padx=15)
        # sets the automatic prediction data clear button to the grid
        self.automatic_prediction_data_clear.grid(row=1, column=0, pady=15, padx=15)
        # sets the automatic prediction data clear label to the grid
        self.automatic_prediction_data_clear_label.grid(row=1, column=1, pady=15, padx=15)
        # sets the clear data on clear images button to the grid
        self.clear_data_on_clear_images_button.grid(row=2, column=0, pady=15, padx=15)
        # sets the clear data on clear images label to the grid
        self.clear_data_on_clear_images_label.grid(row=2, column=1, pady=15, padx=15)
        # sets the save images output button to the grid - skylar
        self.save_images_output_button.grid(row=3, column=0, pady=15, padx=15)
        # sets the save images output label to the grid
        self.save_images_output_label.grid(row=3, column=1, pady=15, padx=15)
        # sets the default settings button to the grid
        self.default_settings_button.grid(row=4, column=0, pady=15, padx=15)

    ####################################################
    # added save images toggle. reloads display for dynamic image and prediction frame
    # uses boolean values -skylar

    '''
    method: reset settings
    resets the settings to default
    '''
    def reset_settings(self):
        # reset the settings
        self.settings.revert_to_default()
        # reconfigure automatic excel_export label
        self.automatic_excel_export_label.config(text=utils.boolean_text_conversion(self.settings.get_automatic_excel_export()))
        # reconfigure prediction data clear label
        self.automatic_prediction_data_clear_label.config(text=utils.boolean_text_conversion(self.settings.get_automatic_prediction_clear_data()))
        # reconfigure clear data on clear images label
        self.clear_data_on_clear_images_label.config(text=utils.boolean_text_conversion(self.settings.get_clear_data_on_clear_images()))
        # reconfigure save images output label
        self.save_images_output_label.config(text=utils.boolean_text_conversion(self.settings.get_save_images_output()))

    '''
    method: close window
    closes the window
    '''
    def close_window(self):
        # close the window
        self.destroy()
        # set the boolean to False to enable a new window
        self.master.is_settings_page_open = False
    '''
    method: run
    runs the settings page
    '''
    def run(self):
        # create the page
        self.create_page()
        # create tooltips
        utils.ToolTips(self.button_dict(),'settings',2)
        # load the page
        self.load_page()
        # set boolean to True to disable a new window
        self.master.is_settings_page_open = True

    '''
    method: toggle label
    param: boolean_string: this represents the value you wish to pass, pass the boolean as a string with no parentheses
    description: toggles a boolean value from the settings class
    '''
    def toggle_label(self,boolean_string,tk_label):
        # split the boolean string by the dots
        code_split_by_dots = boolean_string.split('.')
        # construct the get code to run
        get_code = f'{code_split_by_dots[0]}.{code_split_by_dots[1]}.get_{code_split_by_dots[2]}()'
        # construct the set code to run
        set_code = f'{code_split_by_dots[0]}.{code_split_by_dots[1]}.set_{code_split_by_dots[2]}'
        # run the get code
        if eval(get_code) == True:
            # set the save images output to false
            eval(f'{set_code}(False)')
            # set the save images output label to off
            tk_label.config(text='Off')
        else:
            # set the save images output to true
            eval(f'{set_code}(True)')
            # set the save images output label to on
            tk_label.config(text='On')


