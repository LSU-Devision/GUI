import tkinter as tk
import webbrowser
from tkinter import ttk,messagebox
import Utilities as utils
from Scrapers import Scraper
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
        self.save_model_selection_button = ttk.Button(self.tab2, text='Save Model Selection', command=None)
        # create the model selection label
        self.model_selection_label = ttk.Label(self.tab2, text=self.master.settings.get_selected_model_name(), font=50)

        self.clear_model_selection_button = ttk.Button(self.tab2, text='Clear Model Selection', command=None)
        # create the save excel output button
        self.save_excel_file_button = ttk.Button(self.tab2, text='Save Excel File', command=self.save_excel_file)
        # create the excel output label
        self.excel_file_label = ttk.Label(self.tab2, text=self.master.settings.get_excel_file_name('substring'), font=50)
        # create the clear excel file button
        self.clear_excel_file_button = ttk.Button(self.tab2, text='Clear Excel File', command=None)
        # create the save output path button
        self.save_output_path_button = ttk.Button(self.tab2, text='Save Output Path', command=None)
        # create the output path label
        self.output_path_label = ttk.Label(self.tab2, text=self.master.settings.get_output_folder_name(), font=50)

        self.clear_output_path_button = ttk.Button(self.tab2, text='Clear Output Path', command=None)

        self.load_save_settings_button = ttk.Button(self.tab2, text='Load Save Settings On Startup', command=lambda : self.toggle_label('self.settings.load_save_settings_on_startup',self.load_save_settings_button_label))

        self.load_save_settings_button_label = ttk.Label(self.tab2, text='Off', font=50)

    def create_tab3(self):
        # create the check version button
        self.check_version_button = ttk.Button(self.tab3, text='Check Version',command=self.check_version)
        # create the user guide button
        self.user_guide_button = ttk.Button(self.tab3, text='User Guide', command=self.open_user_guide)

    def create_protocols(self):
        # eliminates duplicate windows
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
    def load_tab1(self):
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
        # sets the save model selection button to the grid
        self.save_model_selection_button.grid(row=0, column=0, pady=15, padx=15)
        # sets the model selection label to the grid
        self.model_selection_label.grid(row=0, column=1, pady=15, padx=15)

        self.clear_model_selection_button.grid(row=0, column=2, pady=15, padx=15)
        # sets the save excel output button to the grid
        self.save_excel_file_button.grid(row=1, column=0, pady=15, padx=15)
        # sets the excel output label to the grid
        self.excel_file_label.grid(row=1, column=1, pady=15, padx=15)

        self.clear_excel_file_button.grid(row=1, column=2, pady=15, padx=15)
        # sets the save output path button to the grid
        self.save_output_path_button.grid(row=2, column=0, pady=15, padx=15)
        # sets the output path label to the grid
        self.output_path_label.grid(row=2, column=1, pady=15, padx=15)

        self.clear_output_path_button.grid(row=2, column=2, pady=15, padx=15)

        self.load_save_settings_button.grid(row=3, column=0, pady=15, padx=15)
        self.load_save_settings_button_label.grid(row=3, column=1, pady=15, padx=15)

    def load_tab3(self):
        # sets the check version button to the grid
        self.check_version_button.grid(row=0, column=0, pady=15, padx=15)
        # load the user guide button to the grid
        self.user_guide_button.grid(row=1, column=0, pady=15, padx=15)




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
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.create_protocols()
        # create tooltips
        utils.ToolTips(self.button_dict(),'settings',2)
        # load the page
        self.load_tab1()
        # load the tab2
        self.load_tab2()
        # load the tab3
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
        scraper_class = Scraper()
        flag1 = scraper_class.check_internet()
        if flag1 is False:
            messagebox.showerror("Error", "No Internet Connection")
            return
        flag2 = scraper_class.check_version()
        if flag2 is True:
            flag2 = messagebox.askyesno("Update", "There is a new version available. Do you want to update?")
            if flag2 is True:
                webbrowser.open(scraper_class.get_update_page())
        else:
            messagebox.showinfo("Update", "You are on the latest version")
            
    
    def open_user_guide(self):
        """
        description: grabs the user guide with checks 
        """
        scraper_user_guide_class = Scraper()
        
        if (scraper_user_guide_class.check_internet())  == False:
            messagebox.showerror("Internet Issue", "Fix your internet to the point where you can load google.com")
            return 
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
            self.geometry('300x200')
        # if the index is 1, resize the tab to 400x400
        elif index == 1:
            # resize the tab
            self.geometry('600x400')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('200x200')

    '''

    '''

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
        excel_file = self.master.excel_editor.get_excel_file()
        if excel_file is not None:
            self.master.settings.set_excel_file_name(excel_file)
            self.excel_file_label.config(text=self.master.excel_editor.get_excel_label())
        else:
            messagebox.showerror("Error", "No Excel File Loaded in the Program, Please Load an Excel File via Excel Window")

