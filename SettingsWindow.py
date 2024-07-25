import tkinter as tk
from tkinter import ttk
import Utilities as utils

'''
Class SettingsWindow
Contributors: Skylar Wilson, Alex Mensen-Johnson
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
        # run the settings page
        self.run()


        '''
        method: create page
        creates the buttons and labels for the settings page and assigns the relative function
        '''
    def create_page(self):
        # create the automatic excel export label
        self.automatic_excel_export_label = ttk.Label(self, text=utils.boolean_text_conversion(self.settings.get_automatic_excel_export()), font=50)
        # create the automatic excel export button
        self.automatic_excel_export = ttk.Button(self, text='Automatic Excel Export', command=self.toggle_automatic_excel_export)
        # create the automatic prediction data clear label
        self.automatic_prediction_data_clear_label = ttk.Label(self,text=utils.boolean_text_conversion(self.settings.get_automatic_prediction_clear_data()),font=50)
        # create the automatic prediction data clear button
        self.automatic_prediction_data_clear = ttk.Button(self,text='Automatic Prediction Data Clear',command=self.toggle_automatic_prediction_data_clear)
        # create the clear data on clear images label
        self.clear_data_on_clear_images_label = ttk.Label(self, text=utils.boolean_text_conversion(self.settings.get_clear_data_on_clear_images()), font=50)
        # create the clear data on clear images button
        self.clear_data_on_clear_images_button = ttk.Button(self, text='Clear Data on Clear Images',command=self.toggle_clear_data_on_clear_images)
        # create the save images output label
        self.save_images_output_label = ttk.Label(self, text=utils.boolean_text_conversion(self.settings.get_save_images_output()), font=50)
        # create the save images output button
        self.save_images_output_button = ttk.Button(self, text='Save images to Output',command=self.toggle_save_images_output)
        # create the reset settings button
        self.default_settings_button = ttk.Button(self, text='Reset To Default Settings',command=self.reset_settings)
        # future button to eliminate duplicate windows
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

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



    '''
    method: toggle automatic excel export
    toggles the automatic excel export on and off
    '''
    def toggle_automatic_excel_export(self):
        if self.settings.get_automatic_excel_export() == True:
        # set the automatic excel export to false
            self.settings.set_automatic_excel_export(False)
            # set the automatic excel export label to off
            self.automatic_excel_export_label.config(text='Off')
        else:
            # set the automatic excel export to true
            self.settings.set_automatic_excel_export(True)
            # set the automatic excel export label to on
            self.automatic_excel_export_label.config(text='On')

    '''
    method: toggle automatic prediction data clear
    toggles the automatic prediction data clear on and off
    '''
    def toggle_automatic_prediction_data_clear(self):
        # toggle the automatic prediction data clear
        if self.settings.get_automatic_prediction_clear_data() == True:
            # set the automatic prediction data clear to false
            self.settings.set_automatic_prediction_clear_data(False)
            # set the automatic prediction data clear label to off
            self.automatic_prediction_data_clear_label.config(text='Off')
        else:
            # set the automatic prediction data clear to true
            self.settings.set_automatic_prediction_clear_data(True)
            # set the automatic prediction data clear label to on
            self.automatic_prediction_data_clear_label.config(text='On')

    '''
    method: toggle clear data on clear images
    toggles the clear data on clear images on and off
    '''
    def toggle_clear_data_on_clear_images(self):
        # toggle the clear data on clear images
        if self.settings.get_clear_data_on_clear_images() == True:
            # set the clear data on clear images to false
            self.settings.set_clear_data_on_clear_images(False)
            # set the clear data on clear images label to off
            self.clear_data_on_clear_images_label.config(text='Off')
        else:
            # set the clear data on clear images to true
            self.settings.set_clear_data_on_clear_images(True)
            # set the clear data on clear images label to on
            self.clear_data_on_clear_images_label.config(text='On')

    ####################################################
    # added save images toggle. reloads display for dynamic image and prediction frame
    # uses boolean values -skylar
    '''
    method: toggle save images output
    toggles the save images output on and off
    '''
    def toggle_save_images_output(self):
        # toggle the save images output
        if self.settings.get_save_images_output() == True:
            # set the save images output to false
            self.settings.set_save_images_output(False)
            # set the save images output label to off
            self.save_images_output_label.config(text='Off')
            # self.update_display()
        else:
            # set the save images output to true
            self.settings.set_save_images_output(True)
            # set the save images output label to on
            self.save_images_output_label.config(text='On')
            # self.update_display()

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
        # load the page
        self.load_page()
        # set boolean to True to disable a new window
        self.master.is_settings_page_open = True
