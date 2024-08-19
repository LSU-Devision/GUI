import tkinter as tk
import webbrowser
from tkinter import ttk,messagebox
import Utilities as utils
from Scrapers import Scraper

class SettingsWindow(tk.Toplevel):
    '''
    :Class: SettingsWindow
    :Contributors: Skylar Wilson, Alex Mensen-Johnson, Sunella Ramnath
    :Description: Settings Window for the main frame
    :Methods:
    init
    create_page
    load_page
    toggle_automatic_excel
    toggle_automatic_prediction_data_clear
    toggle_clear_data_on_clear_images
    toggle_save_images
    reset_settings
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
        # create the third tab
        self.tab3 = ttk.Frame(self.notebook)
        # add the Basic tab
        self.notebook.add(self.tab1, text="Basic", )
        # add the Advanced tab
        self.notebook.add(self.tab2, text="File Save")
        # add the Program tab
        self.notebook.add(self.tab3, text="Program")
        # bind the tab change
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # run the settings page
        self.run()


        '''
        method: create page
        creates the buttons and labels for the settings page and assigns the relative function
        '''
    def create_tab1(self):
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

    def create_tab2(self):
        # create the save model selection button
        self.save_model_selection_button = ttk.Button(self.tab2, text='Save Model Selection', command=self.save_model_selection)
        # create the model selection label
        self.model_label = ttk.Label(self.tab2, text=self.master.settings.get_model_name('string'), font=50)
        # create the clear model selection button
        self.clear_model_selection_button = ttk.Button(self.tab2, text='Clear Model Selection', command=self.clear_model_selection)
        # create the save excel output button
        self.save_excel_file_button = ttk.Button(self.tab2, text='Save Excel File', command=self.save_excel_file)
        # create the excel output label
        self.excel_file_label = ttk.Label(self.tab2, text=self.master.settings.get_excel_file_name('string'), font=50)
        # create the clear excel file button
        self.clear_excel_file_button = ttk.Button(self.tab2, text='Clear Excel File', command=self.clear_excel_file)
        # create the save output path button
        self.save_output_path_button = ttk.Button(self.tab2, text='Save Output Path', command=self.save_output_folder)
        # create the output path label
        self.output_path_label = ttk.Label(self.tab2, text=self.master.settings.get_output_folder_name('string'), font=50)
        # create the clear output path button
        self.clear_output_path_button = ttk.Button(self.tab2, text='Clear Output Path', command=self.clear_output_folder)
        # create the load save settings button
        self.load_save_settings_button = ttk.Button(self.tab2, text='Load Save Settings On Startup', command=lambda : self.load_settings_toggle_wrapper('self.settings.load_save_settings_on_startup',self.load_save_settings_button_label))
        # create the load save settings label
        self.load_save_settings_button_label = ttk.Label(self.tab2, text=utils.boolean_text_conversion(self.master.settings.get_load_save_settings_on_startup()), font=50)
        # create the clear save settings button
        self.clear_save_settings_button = ttk.Button(self.tab2, text='Clear Save Settings', command= self.master.settings.clear_saves)

    def create_tab3(self):
        # create the check version button
        self.check_version_button = ttk.Button(self.tab3, text='Check Version',command=self.check_version)
        # create the user guide button
        self.user_guide_button = ttk.Button(self.tab3, text='User Guide', command=self.open_user_guide)

    def create_protocols(self):
        # eliminates duplicate windows
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())



    def button_dict(self):
        """
        method: button_dict
        description: returns a dictionary of all the buttons in the window
        :return:
        """
        return {
            'automatic_export_to_excel': self.automatic_excel_export,
            'automatic_clear_data_on_predict': self.automatic_prediction_data_clear,
            'clear_data_when_clearing_images': self.clear_data_on_clear_images_button,
            'save_images_to_output': self.save_images_output_button,
            'reset_to_default_settings': self.default_settings_button
        }

    def load_tab1(self):
        """
        :method: load tab 1
        :description: creates the buttons and labels for the basic settings Tab and positions them on the grid
        :return: Nothing
        """
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


    def load_tab2(self):
        """
        :method: load tab 2
        :description: creates the buttons and labels for the File Save settings Tab and postions them on the grid
        :return: Nothing
        """
        # sets the save model selection button to the grid
        self.save_model_selection_button.grid(row=0, column=0, pady=15, padx=15)
        # sets the model selection label to the grid
        self.model_label.grid(row=0, column=1, pady=15, padx=15)
        # sets the clear model selection button to the grid
        self.clear_model_selection_button.grid(row=0, column=2, pady=15, padx=15)
        # sets the save excel output button to the grid
        self.save_excel_file_button.grid(row=1, column=0, pady=15, padx=15)
        # sets the excel output label to the grid
        self.excel_file_label.grid(row=1, column=1, pady=15, padx=15)
        # sets the clear excel output button to the grid
        self.clear_excel_file_button.grid(row=1, column=2, pady=15, padx=15)
        # sets the save output path button to the grid
        self.save_output_path_button.grid(row=2, column=0, pady=15, padx=15)
        # sets the output path label to the grid
        self.output_path_label.grid(row=2, column=1, pady=15, padx=15)

        self.clear_output_path_button.grid(row=2, column=2, pady=15, padx=15)
        # sets the load save settings button to the grid
        self.load_save_settings_button.grid(row=3, column=0, pady=15, padx=15)
        # sets the load save settings label to the grid
        self.load_save_settings_button_label.grid(row=3, column=1, pady=15, padx=15)
        # sets the clear save settings button to the grid
        self.clear_save_settings_button.grid(row=3, column=2, pady=15, padx=15)


    def load_tab3(self):
        """
        :method: load tab 3
        :description: creates the buttons and labels for the User Guide Tab and postions them on the grid
        :return: Nothing
        """
        # sets the check version button to the grid
        self.check_version_button.grid(row=0, column=0, pady=15, padx=15)
        # load the user guide button to the grid
        self.user_guide_button.grid(row=1, column=0, pady=15, padx=15)

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


    def close_window(self):
        """
        :method: close window
        :description: closes the window
        :return:
        """
        # close the window
        self.destroy()
        # set the boolean to False to enable a new window
        self.master.is_settings_page_open = False

    def run(self):
        """
        :method: run
        :description: runs the settings page
        :return:
        """
        # create tab 1
        self.create_tab1()
        # create tab 2
        self.create_tab2()
        # create tab 3
        self.create_tab3()
        # create protocols for the window
        self.create_protocols()
        # create tooltips
        utils.ToolTips(self.button_dict(),'settings',2)
        # load tab 1
        self.load_tab1()
        # load tab2
        self.load_tab2()
        # load tab3
        self.load_tab3()
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


    def check_version(self):
        """
        :method: check version
        :description: checks if there is a new version
        :return: Nothing
        """
        # create the scraper class
        scraper_class = Scraper()
        # check if there is an internet connection
        if scraper_class.check_internet() is False:
            # if there is no internet connection, show an error
            messagebox.showerror("Error", "No Internet Connection")
            return
        # check if there is a new version
        if scraper_class.check_version() is True:
            # if there is a new version, ask if the user wants to update
            flag = messagebox.askyesno("Update", "There is a new version available. Do you want to update?")
            if flag is True:
                # open the update page
                webbrowser.open(scraper_class.get_update_page())
        # if there is no new version show an info box
        else:
            messagebox.showinfo("Update", "You are on the latest version")
            
    
    def open_user_guide(self):
        """
        :method: open user guide
        description: grabs the user guide with checks 
        """
        scraper_user_guide_class = Scraper()
        # check if there is an internet connection
        if (scraper_user_guide_class.check_internet())  == False:
            # if there is no internet connection, show an error
            messagebox.showerror("Internet Issue", "Fix your internet to the point where you can load google.com")
            return
        # open the user guide page
        else: scraper_user_guide_class.get_user_guide()

    def resize_tab(self, index):
        """
        method: resize tab
        description: method to resize the tab
        :param index: index of the current tab
        """
        # if the index is 0, resize the tab to 300x200
        if index == 0:
            # resize the tab
            self.geometry('300x300')
        # if the index is 1, resize the tab to 400x400
        elif index == 1:
            # resize the tab
            self.geometry('600x400')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('200x200')

    def on_tab_change(self, event):
        """
        method: on tab change
        description: method to resize the tab
        """
        # get the index of the tab
        tab_index = self.notebook.index(self.notebook.select())
        # resize the tab
        self.resize_tab(tab_index)

    def save_excel_file(self):
        """
        :method: save excel file
        :description: saves the excel file to the default settings JSON file
        :return: Nothing
        """
        # get the excel file
        excel_file = self.master.excel_editor.get_excel_file()
        # check if there is an excel file
        if excel_file is not None:
            # ask if the user wants to replace the excel file
            if self.master.settings.get_excel_file_name() is not None:
                user_answer = messagebox.askyesno("Save Excel File", "Do you want to replace your current excel file?")
                # if the user does not want to replace the excel file, return
                if user_answer is False:
                    return
            # set the excel file name in the settings
            self.master.settings.set_excel_file_name(excel_file)
            # save the excel file
            self.excel_file_label.config(text=self.master.excel_editor.get_excel_label())
        # if there is no excel file, show an error
        else:
            messagebox.showerror("Error", "No Excel File Loaded in the Program, Please Load an Excel File via Excel Window")

    def clear_excel_file(self):
        """
        :method: clear excel file
        :description: clears the excel file
        :return:
        """
        # clear the excel file from the excel editor
        self.master.excel_editor.set_excel_file(None)
        # clear the excel file name from the settings
        self.master.settings.set_excel_file_name(None)
        # clear the excel file label
        self.excel_file_label.config(text='')
        # clear the excel label title
        self.master.excel_label_title.config(text='None')

    def load_settings_toggle_wrapper(self,boolean_string,tk_label):
        """
        :method: load settings toggle wrapper
        :description: wrapper for the load save settings toggle
        :param boolean_string: string containing the load save settings boolean
        :param tk_label: load save settings boolean
        :return: Nothing
        """
        # toggle the load save settings
        self.toggle_label(boolean_string,tk_label)
        # update the settings
        if self.master.settings.get_load_save_settings_on_startup() is False:
            self.output_path_label.config(text='None')
            self.model_label.config(text='None')
            self.excel_file_label.config(text='None')
        else:
            self.output_path_label.config(text=self.master.settings.get_output_folder_name())
            self.model_label.config(text=self.master.settings.get_model_name())
            self.excel_file_label.config(text=self.master.settings.get_excel_file_name())

    def save_model_selection(self):
        """
        :method: save model selection
        :description: saves the model selection
        :return:
        """
        if self.master.model_path is not None:
            self.master.settings.set_model_name(utils.model_path_to_name(self.master.model_path))
            self.master.settings.set_model_path(self.master.model_path)
            self.model_label.config(text=self.master.settings.get_model_name())
        else:
            messagebox.showerror("Error", "No Model Loaded in the Program, Please Load a Model via Model Dropdown")

    def clear_model_selection(self):
        """
        :method: clear model selection
        :description: clears the model selection
        :return:
        """
        self.master.settings.set_model_name(None)
        self.master.settings.set_model_path(None)
        self.model_label.config(text='None')

    def save_output_folder(self):
        """
        :method: save output folder
        :description: saves the output folder
        :return:
        """
        if self.master.excel_editor.get_output_folder() is not self.master.settings.get_output_folder_name():
            self.master.settings.set_output_folder_name(self.master.excel_editor.get_output_folder())
            self.output_path_label.config(text=self.master.excel_editor.get_output_folder())
        else:
            messagebox.showerror("Error", "Current output folder is already saved")

    def clear_output_folder(self):
        """
        :method: clear output folder
        :description: clears the output folder
        :return:
        """
        self.master.excel_editor.set_output_folder('output')
        self.master.settings.set_output_folder_name('output')
        self.output_path_label.config(text='output')