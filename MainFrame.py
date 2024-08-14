import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tensorflow as tf
import os.path
from stardist.models import StarDist2D
import matplotlib
from Slideshow import Slideshow
import Settings
import sys
import ExcelEditor as excel_editor
from SettingsWindow import SettingsWindow
from Predictions import Predictions
from ExcelWindow import ExcelWindow
import Utilities as utils

matplotlib.use('agg')

'''
Class Main Frame
Author: Max
Contributors: Skylar Wilson, Alex Mensen-Johnson, Sunella Ramnath
Class: Main Frame
Description: Main Frame of GUI, all sub frames will be loaded inside of this class
Params:
    container: a container containing the title and geometry of the Graphic User Interface
Methods:
    init: Initialization method
    create display: method to create the buttons and subframes of the main frame
    load display: method to load data into the GUI
    select files: method for selecting files to be predicted on
    select model: method for selecting the model for prediction
    predict: method for predicting egg count for the frog eggs. outputs the photos saved with the number count
    predict all: predicts the values of all the loaded files in the GUI
    clear images: Clears the images from the GUI
    help page: creates a help page pop up for the users
'''


class MainFrame(ttk.Frame):
    """
    Class Main Frame
    Author: Max
    Contributors: Skylar Wilson, Alex Mensen-Johnson, Sunella Ramnath
    Class: Main Frame
    Description: Main Frame of GUI, all sub frames will be loaded inside of this class
    Params:
        container: a container containing the title and geometry of the Graphic User Interface
    Methods:
        init: Initialization method
        create display: method to create the buttons and subframes of the main frame
        load display: method to load data into the GUI
        select files: method for selecting files to be predicted on
        select model: method for selecting the model for prediction
        predict: method for predicting egg count for the frog eggs. outputs the photos saved with the number count
        predict all: predicts the values of all the loaded files in the GUI
        clear images: Clears the images from the GUI
        help page: creates a help page pop up for the users
    """

    def __init__(self, container):
        """
        method: init
        description: Initialization method
        :param container:
        """
        # initialize the container's parant init methods
        super().__init__(container)
        # initialize the settings
        self.settings = Settings.SettingsJson()
        # initialize the container method
        self.container = container
        # create the image files list, set to empty
        self.image_files = []
        # create the prediciton files, leave them empty
        self.prediction_files = {}
        # initialize predictions_data list -skylar
        self.predictions_data = []
        # variable for the model
        self.model = None
        # initialize the excel editor class
        self.excel_editor = excel_editor.ExcelEditor(master=self)
        # set the excel file to none
        self.excel_editor.set_excel_file(None)
        # set the excel label to none
        self.excel_editor.set_excel_label(None)
        # initialize the excel label index
        self.excel_label_index = 0
        # boolean checker to see if the excel window is open
        self.is_excel_save_page_open = False
        # boolean checker to see if the settings window is open
        self.is_settings_page_open = False
        # set the device's GPU
        self.device = '/GPU:0' if tf.config.experimental.list_physical_devices('GPU') else '/CPU:0'
        # initialize the progress popup to None
        self.progress_popup = None
        # set the model path to nothing
        self.model_path = ''
        # settings for automatic excel export
        self.automatic_excel_setting = self.settings.get_automatic_excel_export()
        # print(self.automatic_excel_setting)
        self.predict_index = 1
        # settings for automatic prediction data clear
        self.automatic_prediction_data_clear_setting = self.settings.get_automatic_prediction_clear_data()
        # settings for clear data on clear images toggle
        self.clear_data_on_clear_images_setting = self.settings.get_clear_data_on_clear_images()
        # settings for save images output toggle -skylar,
        self.save_images_output_setting = self.settings.get_save_images_output()
        # Create an instance of the Predictions class
        self.predictions = Predictions(self.image_files, self, self.model, self)
        # boolean checker to see if the data has been cleared
        self.is_data_cleared = True
        # create all the buttons for the display
        self.create_display()
        # add tooltips
        utils.ToolTips(self.button_dict(), 'main_frame', 2)
        # load the display
        self.load_display()
        # empty variable for excel window
        self.excel_window = None

    def create_display(self):
        """
        Creates the display in the code and organizes all the creation into a method
        If you intend on creating a feature for display, add it here please
        :return:
        """
        # Creates the select files button
        self.select_files_button = ttk.Button(self, text='Select Files', command=self.select_files)
        # Creates the slide show
        self.slideshow = Slideshow(self)
        # initialize buttons as disabled until a model is selected
        self.model_selected = False
        # Creates the predict all button
        self.predict_all_button = ttk.Button(self, text='Predict All', command=self.predictions.predict_all,
                                             state=tk.DISABLED)
        # make two buttons
        # self.select_model_button = ttk.Button(self, text='Select Model Folder', command=self.select_model)
        self.select_model_dropdown = ttk.Combobox(self, state='readonly', values=
        [
            'Frog Egg Counter',
            'Oyster Seed Counter',
            'Frog Egg Classification',
            'Select Model Folder Manually'
        ])

        self.select_model_dropdown.set('Select Model')

        self.select_model_dropdown.bind('<<ComboboxSelected>>', lambda event: self.get_model_by_dropdown())
        # creates the model label
        self.model_label = ttk.Label(self, text='No Model Selected', font=50)
        # creates clear button
        self.clear_button = ttk.Button(self, text='Clear Images', command=self.clear_images)
        # creates a help button that will display button usage
        self.show_info = ttk.Button(self, text='Help', command=self.help_page)
        # creates the excel label
        self.excel_label_title = ttk.Label(self, text=str(self.excel_editor.get_excel_label()), font=50)
        # creates the export to excel button
        self.excel_window_button = ttk.Button(self, text='Excel Window', command=lambda: self.open_excel_window())
        # Create settings page
        self.settings_page_button = ttk.Button(self, text='Settings', command=lambda: self.open_settings_window())


    def button_dict(self):
        """
        method: button_dict
        Author: Alex Mensen-Johnson
        :return: a dictionary of all the buttons for the creation of tooltips
        """
        return {
            'select_model': self.select_model_dropdown,
            'select_files': self.select_files_button,
            'predict_all': self.predict_all_button,
            'clear_images': self.clear_button,
            'help': self.show_info,
            'excel window': self.excel_window_button,
            'settings_window': self.settings_page_button
        }

    def load_display(self):
        """
        method: load_display
        Author: Alex Mensen-Johnson
        organizes the display buttons into a method for loading the display in a clear format
        If you are loading anything into the display, please add it here.
        :return:
        """
        # using grid layout -skylar
        self.grid_rowconfigure(0, weight=0)
        # using grid layout -skylar
        self.grid_columnconfigure(0, weight=1)
        # loads the model label into the frame
        self.model_label.grid(row=1, column=0, pady=5)
        # loads the select model button into the frame
        #self.select_model_button.grid(row=2, column=0, pady=5)
        self.select_model_dropdown.grid(row=2, column=0, pady=5)
        # Loads the select files button into the page
        self.select_files_button.grid(row=3, column=0, pady=5)
        # loads the predict all button
        self.predict_all_button.grid(row=4, column=0, pady=5)
        # loads the slide show frame into the display
        self.slideshow.grid(row=5, column=0)
        # adds clear button using grid method
        self.clear_button.grid(row=6, column=0, pady=5)
        # adds the button to the GUI
        self.show_info.grid(row=7, column=0, pady=5)
        # adds the excel label to the window
        self.excel_label_title.grid(row=8, column=0, pady=0)
        # adds the excel save page to the window
        self.excel_window_button.grid(row=9, column=0, pady=5)
        # adds the settings button to the window
        self.settings_page_button.grid(row=10, column=0, pady=5)



    def update_display(self):
        """
        method: update_display
        Author: Skylar Wilson
        Destroys current frame and reloads MainFrame for the purpose of dynamic display.
        :return:
        """
        # make the parent container the same container
        parent_container = self.container
        # destroy the mainframe window
        self.destroy()
        # Re-initialize the frame with the same container
        new_frame = MainFrame(parent_container)
        # Add the new frame to the container using grid
        new_frame.grid(row=0, column=0, sticky='nsew')

    def disable_button(self, button):
        """
        method: disable_button
        Author: Skylar Wilson
        :param button: the button that will be disabled
        """
        # Disable the button
        button.config(state=tk.DISABLED)

    def enable_button(self, button):
        """
        method: enable_button
        Author: Skylar Wilson
        :param button: the button that will be enabled
        """
        # Enables the button
        button.config(state=tk.NORMAL)

    def select_files(self):
        """
        method: select_files
        Author: Max, Alex Mensen-Johnson
        allows the user to manually select files to be predicted
        :return:
        """
        # opens the dialog box for the user to select files
        files = filedialog.askopenfilenames(initialdir='/home/max/development/stardist/data')
        # initialize an empty list to hold the files
        file_list = []
        # loop through the selected files
        for image in files:
                answer = utils.check_file_extension(image, 'image')
                # if the user does not want to continue, move to the next iteration of the loop
                if answer == True:
                    # move to the next iteration of the loop
                    continue
                elif answer == False:
                    return
                else:
                    # append the image to the list
                    file_list.append(image)
        # add files to the image files variables
        self.image_files.extend(file_list)
        # update the predictions image files
        self.predictions.image_files = self.image_files
        # if the files exist
        if self.image_files:
            # update the slideshow
            self.slideshow.update_image()

    def get_model_by_dropdown(self):
        """
        method: get_model_by_dropdown
        Author: Max, Alex Mensen-Johnson
        description: gets the model from the dropdown
        :return: Nothing
        """
        # get the model from the dropdown
        model_option = self.select_model_dropdown.get()
        # print the model
        print(f'{model_option} model selected')
        # if the model is not selected, return
        if model_option == 'Select Model':
            return
        # if the model is selected manually
        elif model_option == 'Select Model Folder Manually':
            # use the file dialog method to manually select the model
            self.model_path = filedialog.askdirectory()
        # If the model is selected from one of the options, load the option
        else:
            self.model_path = Predictions.get_model_path(self.predictions, model_option)
        # print the model path
        print(self.model_path)
        # print the full file name of the model path
        print(os.path.basename(self.model_path))
        # print the directory of the model path
        print(os.path.dirname(self.model_path))
        # open the model with tensorflow
        with tf.device(self.device):
            # set the model to the stardist model
            self.model = StarDist2D(None, name=os.path.basename(self.model_path),
                                    basedir=os.path.dirname(self.model_path))
        # change prediction model to the current model
        self.predictions.model = self.model
        # configure the label to display the model
        self.model_label.config(text=f'Current Model: {os.path.basename(self.model_path)}')
        # if the model is selected, then enable the button
        if not self.model_selected:
            # enable the predict all button
            self.predict_all_button.config(state=tk.NORMAL)
            # ste the model selected to true
            self.model_selected = True

    def clear_images(self):
        """
        method: clear_images
        Author:Alex Mensen-Johnson
        clears the images from the GUI
        """
        # Set the base image reference to None
        self.slideshow.base_image.image_ref = None
        # Clear the label of the file path above the slideshow
        self.slideshow.filepath_label.config(text='')
        # Set the index of the pictures to 0
        self.slideshow.current_index = 0
        # empty the image files array
        self.image_files = []
        # set the image to none
        self.slideshow.base_image.set_image(None)
        # set the image files to the current image files, which is none
        self.slideshow.image_files = self.image_files
        # set the predicted image to none
        self.slideshow.predicted_image.set_image(None)
        # set the item count label to empty
        self.slideshow.item_count_label.config(text=' ')
        # resets the predictions file to the empty dictionary
        self.predictions.prediction_files = {}

        # sets the prediction files to empty
        self.prediction_files = {}
        # sets the slideshow prediction files to empty
        self.slideshow.prediction_files = self.prediction_files
        # reset the slideshow index
        self.slideshow.current_index = 0
        # display a message box showing the Images are cleared
        messagebox.showinfo("Devision", "Images Cleared!")
        # check the settings variable
        if self.settings.get_clear_data_on_clear_images():
            # clear the data
            self.clear_predicted_data()

    def help_page(self):
        """
        Help Page: by Alex Mensen-Johnson
        Description: Loads the Help_Information.txt into a file, reads the file, and displays the information in a pop up
        """
        # Load File
        info_file = open(utils.resource_path("docs/Help_Information.txt"))
        # Read the file
        file_information = info_file.read()
        # Create the title string
        title = 'Help'
        # Create pop up with the information
        messagebox.showinfo(title, file_information)

    def clear_predicted_data(self):
        """
        clear the predicted data
        :return: no return
        """
        # clear the predictions data
        self.predictions.predictions_data.clear()
        # set the is data cleared variable to True
        self.is_data_cleared = True
        # display a message box showing the data is cleared
        messagebox.showinfo("Devision", "Data Cleared")

    def open_excel_window(self):
        """
        method: opens the excel window if an instance is not already open
        :return:
        """
        # check if the excel window is already open
        if self.is_excel_save_page_open == False:
            # open the excel window
            self.excel_window = ExcelWindow(master=self, container=self.container, excel_editor=self.excel_editor)

    def open_settings_window(self):
        """
        method: open_settings_window
        description: opens the settings window if it is not already open
        :return:
        """
        # check if the settings window is already open
        if self.is_settings_page_open == False:
            # open the settings window
            SettingsWindow(master=self, container=self.container, settings=self.settings)
