import tkinter as tk
from tkinter import ttk, messagebox,filedialog
import Utilities as utils
import os

class ExcelWindow(tk.Toplevel):
    """
    Class: ExcelWindow
    Contributors: Alex Mensen-Johnson, Sunella Ramnath
    Description: Class for the Excel Window
    Params:
        master = master class aka MainFrame
        container = container class
        excel_editor = excel editor class
    methods:
        init: initialize the class
        create_page: create the page
        load_page: load the page
        close_window: close the window
        run: run the create and load methods
    """
    def __init__(self, master=None , container=None, excel_editor=None):
        """
        method: init
        description: initialize the class
        :param master: Mainframe class from MainFrame.py
        :param container: container of the Mainframe class
        :param excel_editor: excel editor class from ExcelEditor.py
        """
        # Initializes the master class
        super().__init__(master=master)
        # saves the master variable locally
        self.master = master
        # sets the container variable for a local reference for the container
        self.container = container
        # sets the excel editor variable for a local reference for the excel editor class
        self.excel_editor = excel_editor
        # copies the size of the main window
        main_window_width = self.container.winfo_width()
        # set the size of the pop up window
        main_window_height = self.container.winfo_height()
        # variables for the pop up window
        pop_up_window_width = 400
        # variables for the pop up window
        pop_up_window_height = 400
        # set the position of the pop up window
        x = main_window_width + 75
        # set the position of the pop up window
        y = main_window_height // 2 - pop_up_window_height // 2  # center the pop-up window vertically
        # set the title of the pop up window
        self.title('Excel Window')


        # set the geometry of the pop up window
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        # checks to see if the excel file is used, creates a substring if so
        if self.excel_editor.get_excel_file() is not None:
            self.excel_editor.get_substring()
        # convert frame into notebook
        self.notebook=ttk.Notebook(self)
        # add the notebook using the grid method
        self.notebook.grid(row=0,column=0)
        # create the first tab
        self.tab1=ttk.Frame(self.notebook)
        # create the second tab
        self.tab2=ttk.Frame(self.notebook)
        # create the third tab
        self.tab3=ttk.Frame(self.notebook)
        # add the Basic tab
        self.notebook.add(self.tab1,text="Basic",)
        # add the Advanced tab
        self.notebook.add(self.tab2,text="Columns")
        # add the File Names tab
        self.notebook.add(self.tab3, text = 'File Names')

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.excel_file_name = tk.StringVar()
        self.output_folder_name = tk.StringVar()
        self.excel_file_variable = None
        self.output_folder_variable = None
        # creates the page
        self.run()

    def create_tab1(self):
        """
        :method: create tab 1
        :description: creates the page
        """
        # create the export excel button
        self.export_excel_button = ttk.Button(self.tab1, text='Export to Excel', command=self.master.excel_editor.export_predictions_to_excel)
        # create the load excel by selection button
        self.load_excel_by_selection_button = ttk.Button(self.tab1, text='Load Excel', command=self.load_excel_by_selection)
        # create the clear predictions button
        self.clear_prediction_data_button = ttk.Button(self.tab1, text='Clear Predictions',command=self.master.clear_predicted_data)
        # create the clear excel file button
        self.clear_excel_file_button = ttk.Button(self.tab1, text='Clear Excel File', command=self.clear_excel_file)

    def create_tab2(self):
        """
        :method: create tab 2
        :description: creates the page
        """
        dropdown_list = ['index', 'date', 'time', 'file_name', 'total_count']

        # creates all the dropdowns using the dropdown builder method
        for dropdown in dropdown_list:
            self.dropdown_builder(dropdown)

        # create the save excel column button
        self.save_excel_column_button = ttk.Button(self.tab2, text='Save Excel Column Order', command=self.save_excel_columns)

    def create_tab3(self):
        """
        :method: create tab 3
        :description: creates the page
        """
        self.excel_name_label = ttk.Label(self.tab3, text='New Excel File Name : ')
        self.excel_name_field= ttk.Entry(self.tab3, textvariable=self.excel_file_name)
        if self.master.excel_editor.get_excel_file() is not None:
            self.excel_name_field.insert(0, os.path.basename(self.master.excel_editor.get_excel_file()).split('.')[0])
        self.excel_name_save_button = ttk.Button(self.tab3, text='Save Excel File Name', command=self.save_excel_file_name)

        self.output_folder_label = ttk.Label(self.tab3,text = 'Output Folder Name : ')
        self.output_folder_field = ttk.Entry(self.tab3, textvariable = self.output_folder_name)
        if self.master.excel_editor.get_output_folder() is not None:
            self.output_folder_field.insert(0, self.master.excel_editor.get_output_folder().split('\\')[0])
        self.output_folder_save_button = ttk.Button(self.tab3, text = 'Save Output Folder Name', command = self.save_output_folder_name)

    def create_protocols(self):
        # eliminates duplicate windows
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def load_tab1(self):
        """
        :method: load tab 1
        :description: creates the buttons and labels for the Basic settings Tab and postions them on the grid
        :return: Nothing
        """
        # creates the export excel button
        self.export_excel_button.grid(row=0, column=0, pady=15, padx=15)
        # creates the load excel by selection button
        self.load_excel_by_selection_button.grid(row=0, column=1, pady=15, padx=15)
        # creates the clear predictions button
        self.clear_prediction_data_button.grid(row=1, column=0, pady=15, padx=15)
        # creates the clear excel file button
        self.clear_excel_file_button.grid(row=1, column=1, pady=15, padx=15)



    def load_tab2(self):
        """
        :method: load tab 2
        :description: creates the buttons and labels for the Advanced settings Tab and postions them on the grid
        :return: Nothing
        """
        self.excel_index_column_label.grid(row=1, column=1, pady=15, padx=15)
        self.excel_index_column_dropdown.grid(row=1, column=2, pady=15, padx=15)

        self.excel_date_column_label.grid(row=2, column=1, pady=15, padx=15)
        self.excel_date_column_dropdown.grid(row=2, column=2, pady=15, padx=15)

        self.excel_time_column_label.grid(row=3, column=1, pady=15, padx=15)
        self.excel_time_column_dropdown.grid(row=3, column=2, pady=15, padx=15)

        self.excel_file_name_column_label.grid(row=4, column=1, pady=15, padx=15)
        self.excel_file_name_column_dropdown.grid(row=4, column=2, pady=15, padx=15)

        self.excel_total_count_column_label.grid(row=5, column=1, pady=15, padx=15)
        self.excel_total_count_column_dropdown.grid(row=5, column=2, pady=15, padx=15)
        # creates the save excel column button
        self.save_excel_column_button.grid(row=6, column=1, pady=15, padx=15)

    def load_tab3(self):
        """
        :method: load tab 3
        :description: creates the buttons and labels for the Advanced settings Tab and postions them on the grid
        :return: Nothing
        """
        self.excel_name_label.grid(row=0, column=0, pady=15, padx=15)
        self.excel_name_field.grid(row=0, column=1, pady=15, padx=15)
        self.excel_name_save_button.grid(row=0, column=2, pady=15, padx=15)

        self.output_folder_label.grid(row=1, column=0, pady=15, padx=15)
        self.output_folder_field.grid(row=1, column=1, pady=15, padx=15)
        self.output_folder_save_button.grid(row=1, column=2, pady=15, padx=15)

    def button_dict(self):
        """
        method: button dict
        description: returns a dictionary of the buttons name strings and the buttons
        :return: dictionary of buttons
        """
        return {
            'export_to_excel': self.export_excel_button,
            'load_excel': self.load_excel_by_selection_button,
            'clear_predictions': self.clear_prediction_data_button,
            'clear_excel_file': self.clear_excel_file_button,
            'excel_index_column': self.excel_index_column_dropdown,
            'excel_date_column': self.excel_date_column_dropdown,
            'excel_time_column': self.excel_time_column_dropdown,
            'excel_file_name_column': self.excel_file_name_column_dropdown,
            'excel_total_count_column': self.excel_total_count_column_dropdown,
            'excel_file_name_field': self.excel_name_field,
            'save_excel_file_name': self.excel_name_save_button,
            'output_folder_name_field': self.output_folder_field,
            'save_output_folder_name': self.output_folder_save_button
        }



    def clear_excel_file(self):
        """
        method: clear excel file
        description: method to clear the excel file from the program
        :return:
        """
        # clear the excel file from the excel editor
        self.master.excel_editor.set_excel_file(None)
        # clear the excel label
        self.master.excel_editor.set_excel_label(None)
        # set the excel label title to none
        self.master.excel_label_title.config(text='None')

    def load_excel_by_selection(self):
        """
        method: load excel by selection
        description: method to load the excel file by selection
        :return:
        """
        # opens the file dialog to select the excel file
        excel_file = filedialog.askopenfilename(initialdir='/home/max/development/stardist/data')
        if utils.check_file_extension(excel_file, 'excel') == False:
            return
        # set the excel file in the excel editor
        self.master.excel_editor.set_excel_file(excel_file)
        # create the substring for the excel file
        self.master.excel_editor.get_substring()
        # set the excel label title to the excel file
        self.master.excel_label_title.config(text= str(self.excel_editor.get_excel_label()))

    def close_window(self):
        """
        method: close window
        description: method to close the window
        :return:
        """
        # close the window
        self.destroy()
        # set the boolean to True to enable a new window
        self.master.is_excel_save_page_open = False

    def run(self):
        """
        method: run
        description: method to run the window
        :return:
        """
        # create the page
        # self.create_page()
        self.create_tab1()

        self.create_tab2()

        self.create_tab3()

        self.create_protocols()
        # create tooltips
        utils.ToolTips(self.button_dict(),'excel_window',2)
        # load the page
        #self.load_page()
        self.load_tab1()
        self.load_tab2()
        self.load_tab3()
        # sets the boolean to true to prevent duplicates of the window
        self.master.is_excel_save_page_open = True

    def save_excel_columns(self):
        """
        method: save excel columns
        description: method to save the Excel columns
        :return: False if the Excel columns have the same column value
        """
        # check list for if the Excel columns have the same column value
        check_list = [self.master.excel_editor.get_excel_index_column_index(),
                      self.master.excel_editor.get_excel_date_column_index(),
                      self.master.excel_editor.get_excel_time_column_index(),
                      self.master.excel_editor.get_excel_file_name_column_index(),
                      self.master.excel_editor.get_excel_total_count_column_index()
                      ]

        # check if the Excel columns have the same column value
        check_value = True
        # check if the Excel columns have the same column value
        for value in check_list:
            # check if the Excel columns have the same column value
            for value2 in check_list[check_list.index(value) + 1:]:
                # check if the Excel columns have the same column value
                if value == value2 and value2 != 'None':
                    # set the check value to false
                    check_value = False
        # if the check value is true, save the Excel columns
        if check_value is True:
            # save the Excel columns
            self.master.excel_editor.save_excel_settings()
            # show a success message
            messagebox.showinfo('Success', 'Excel Columns Saved')
        # if the check value is false, show an error message
        else:
            # show an error message
            messagebox.showerror('Error', 'Excel Columns have the same column value, cannot save')
            # return the function
            return False


    def resize_tab(self,index):
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
            self.geometry('400x350')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('500x200')

    '''
    
    '''
    def on_tab_change(self,event):
        """
        method: on tab change
        description: method to resize the tab
        """
        # get the index of the tab
        tab_index = self.notebook.index(self.notebook.select())
        # resize the tab
        self.resize_tab(tab_index)


    def save_excel_file_name(self):
        """
        method: save Excel file name
        description: method to save the Excel file name
        """
        # call the string checker class
        checker = utils.StringChecker()
        # conditional statement to check the given string
        if checker.filename_checker(self.excel_name_field.get()) is False:
            # save the Excel file name to the variable
            if self.master.settings.get_output_folder_name() is not None:
                self.master.excel_editor.set_excel_file(self.excel_name_field.get())
            else:
                self.master.settings.set_output_folder_name('output')
                self.master.excel_editor.set_excel_file(self.excel_name_field.get())
            # show a success message
            messagebox.showinfo("Success", "Excel File Name Saved")
        # conditional statement to check the given string
        else:
            # show an error message, ask the user if they want to see what characters or names are invalid
            flag = messagebox.askokcancel("Error", "Filename cannot be used.\nFilename contains invalid characters or "
                                                   "names that cannot be used or is empty. \nDo you want to see what "
                                                   "characters or names are invalid?")
            # if the flag is true, show the invalid characters or names
            if flag is True:
                # show the invalid characters or names
                messagebox.showinfo("Invalid naming conventions", 'Invalid characters: \n' + checker.get_invalid_characters_string() + '\nInvalid names: \n' + checker.get_reserved_filenames_string() + '\nAlso file names cannot end with periods or spaces')

    def save_output_folder_name(self):
        checker = utils.StringChecker()

        if checker.folder_checker(self.output_folder_field.get()) is False:
            self.master.excel_editor.set_output_folder(self.output_folder_field.get())
            if self.master.excel_editor.get_excel_file() is not None:
                self.master.excel_editor.set_excel_file(self.master.excel_editor.get_excel_file())
            messagebox.showinfo("Success", "Output Folder Name Saved")
        else:
            flag = messagebox.askyesno("Error","Folder name cannout be used.\nFolder name contains invalid "
                                               "characters, is empty, is too long, or begins/ends with a space.\nDo "
                                               "you want to see the permissable naming conventions allowed?")
            if flag is True:
                messagebox.showinfo("Naming conventions",f'Acceptable characters \n Letters, Numbers, underscore, hyphen, and spaces are allowed\nFolder name cannot begin with or end with a space')


    def get_excel_file_variable(self):
        return self.excel_file_variable

    def set_excel_file_variable(self, excel_file):
        self.excel_file_variable = excel_file

    def dropdown_builder(self,column_name='index'):
        code_string = f'self.excel_{column_name}_column_label = ttk.Label(self.tab2, text="Excel {column_name.title()} Column")\n'\
        f'self.excel_{column_name}_column_dropdown = ttk.Combobox(self.tab2, state="readonly",values=["None", "1", "2", "3", "4", "5"])\n'\
        f'self.excel_{column_name}_column_dropdown.set(self.excel_editor.get_excel_{column_name}_column_index())\n'\
        f'self.excel_{column_name}_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_{column_name}_column_value(self.excel_{column_name}_column_dropdown.get()))'
        exec(code_string,locals(),globals())
