import tkinter as tk
import webbrowser
from tkinter import ttk,messagebox
import Utilities as utils
from Scrapers import Scraper

class SettingsWindow(tk.Toplevel):
    '''
    :Class: SettingsWindow
    :Contributors: Skylar Wilson, Alex Mensen-Johnson, Sunella Ramnath, Paul Yeon
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

        #self.info2 = None
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
        # set the minimum size for resizing
        self.minsize(pop_up_window_width, pop_up_window_height)
        # set the geometry of the pop up window
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        # convert frame into notebook
        self.notebook = ttk.Notebook(self)
        # add the notebook using the grid method
        self.notebook.grid(row=0, column=0)
        
        # create the first tab
        self.tab1 = self.BasicFrame(self.notebook)
        # create the third tab
        self.tab3 = ttk.Frame(self.notebook)
        # create the fourth tab
        
        # add the Basic tab
        self.notebook.add(self.tab1, text=self.tab1.title)
        # add the Advanced tab
        self.notebook.add(self.tab2, text=self.tab2.title)
        # add the Program tab
        self.notebook.add(self.tab3, text="Program")
        # add the Style tab
        self.notebook.add(self.tab4, text=self.tab4.title)
                
        # bind the tab change
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # run the settings page
        self.run()


        '''
        method: create page
        creates the buttons and labels for the settings page and assigns the relative function
        '''
    class BasicFrame(ttk.Frame):
        def __init__(self, *args, kwargs={}):
            super().__init__(*args, **kwargs)
            # TODO: Frame must be resized
            self._title = 'Basic'
            
            # TODO: Button commands must be switched to toggle label
            self.__button_kwargs = {'command' : None}
            self.__label_kwargs = {"font":"TkDefaultFont"}
            self.__g_kwargs = {"padx":15, "pady":15}
            self.__args = [self]
            
            button_individuals = [
                {"text":"Reset to Default Settings"},
                {"text":"Automatic Clear Last Prediction on Predict"},
                {"text":"Automatic Export to Excel"},
                {"text":"Clear Predictions when Clearing Images"},
                {"text":"Save Images to Output"}
            ]
            
            label_individuals = [
                {"text":"Click buttons to toggle settings"},
                {"text":"On/Off placeholder"},
                {"text":"On/Off placeholder"},
                {"text":"On/Off placeholder"},
                {"text":"On/Off placeholder"}
            ]
            
            args = self.__args
            kwargs = self.__button_kwargs
            
            self._b_widgets = []
            for b_kwargs in button_individuals:
                current_kwargs = kwargs.copy()
                current_kwargs.update(b_kwargs)
                
                self._b_widgets.append(
                    ttk.Button(*args, **current_kwargs)
                )
           
            kwargs = self.__label_kwargs
            self._l_widgets = []
            for l_kwargs in label_individuals:
                current_kwargs = kwargs.copy()
                current_kwargs.update(l_kwargs)
                
                self._l_widgets.append(
                    ttk.Label(*args, **current_kwargs)
                )
            
            kwargs = self.__g_kwargs
            [x.grid(row=i, column=0, **kwargs) for i, x in enumerate(self._b_widgets)]
            [x.grid(row=i, column=1, **kwargs) for i, x in enumerate(self._l_widgets)]
        
        @property
        def title(self):
            return self._title
            
    def create_tab2(self):
        self.info2 = tk.Label(self.tab2, text="Click buttons to toggle settings", font=50)

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
        self.save_output_folder_button = ttk.Button(self.tab2, text='Save Output Folder', command=self.save_output_folder)
        # create the output path label
        self.output_folder_label = ttk.Label(self.tab2, text=self.master.settings.get_output_folder_name('string'), font=50)
        # create the clear output path button
        self.clear_output_folder_button = ttk.Button(self.tab2, text='Clear Output Path', command=self.clear_output_folder)
        # create the load save settings button
        self.load_save_settings_button = ttk.Button(self.tab2, text='Load Save Settings On Startup', command=lambda : self.toggle_label('self.settings.load_save_settings_on_startup',self.load_save_settings_button_label))
        # create the load save settings label
        self.load_save_settings_button_label = ttk.Label(self.tab2, text=utils.boolean_text_conversion(self.master.settings.get_load_save_settings_on_startup()), font=50)
        # create the clear save settings button
        self.clear_save_settings_button = ttk.Button(self.tab2, text='Clear Save Settings', command= self.clear_save_settings)

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
            'reset_to_default_settings': self.default_settings_button,
            'save_model_selection': self.save_model_selection_button,
            'model_selection_label': self.model_label,
            'clear_model_selection': self.clear_model_selection_button,
            'save_excel_file': self.save_excel_file_button,
            'excel_file_label': self.excel_file_label,
            'clear_excel_file': self.clear_excel_file_button,
            'save_output_folder': self.save_output_folder_button,
            'output_folder_label': self.output_folder_label,
            'clear_output_folder': self.clear_output_folder_button,
            'load_save_settings_on_startup': self.load_save_settings_button,
            'clear_save_settings': self.clear_save_settings_button,
            'check_version': self.check_version_button,
            'user_guide': self.user_guide_button
        }

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
        # create tab 3
        self.create_tab3()
        # create protocols for the window
        self.create_protocols()
        # create tooltips
        # utils.ToolTips(self.button_dict(),'settings',2)
        
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
            self.geometry('400x400')
        # if the index is 1, resize the tab to 400x400
        elif index == 1:
            # resize the tab
            self.geometry('600x500')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('200x300')

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
        # clear the excel file name from the settings
        self.master.settings.set_excel_file_name(None)
        # clear the excel file label
        self.excel_file_label.config(text='None')

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
            self.output_folder_label.config(text=self.master.excel_editor.get_output_folder())
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
        self.output_folder_label.config(text='output')

    def clear_save_settings(self):
        """
        :method: clear save settings
        :description: clears the save settings
        :return:
        """
        self.clear_excel_file()
        self.clear_model_selection()
        self.clear_output_folder()