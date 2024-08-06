import tkinter as tk
from tkinter import ttk, messagebox,filedialog
import Utilities as utils

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
        self.excel_file_variable = None
        # creates the page
        self.run()
    def create_page(self):
        """
        method: create_page
        description: creates the page
        """
        # create the export excel button
        self.export_excel_button = ttk.Button(self.tab1, text='Export to Excel', command=self.master.excel_editor.export_predictions_to_excel)
        # create the load excel by selection button
        self.load_excel_by_selection_button = ttk.Button(self.tab1, text='Load Excel', command=self.load_excel_by_selection)
        # create the clear predictions button
        self.clear_prediction_data_button = ttk.Button(self.tab1, text='Clear Predictions',command=self.master.clear_predicted_data)
        # create the clear excel file button
        self.clear_excel_file_button = ttk.Button(self.tab1, text='Clear Excel File', command=self.clear_excel_file)
        # protocol for closing the window
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        # create the excel index column
        self.excel_index_column_label = ttk.Label(self.tab2, text='Excel Index Column')
        # create the excel index column dropdown
        self.excel_index_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel index column dropdown to the current value
        self.excel_index_column_dropdown.set(self.excel_editor.get_excel_index_column_index())
        # bind the event to the excel index column dropdown
        self.excel_index_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_index_column_value(self.excel_index_column_dropdown.get()))

        # create the excel date column
        self.excel_date_column_label = ttk.Label(self.tab2, text='Excel Date Column')
        # create the excel date column dropdown
        self.excel_date_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel date column dropdown to the current value
        self.excel_date_column_dropdown.set(self.excel_editor.get_excel_date_column_index())
        # bind the event to the excel date column dropdown
        self.excel_date_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_date_column_value(self.excel_date_column_dropdown.get()))

        # create the excel time column
        self.excel_time_column_label = ttk.Label(self.tab2, text='Excel Time Column')
        # create the excel time column dropdown
        self.excel_time_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel time column dropdown to the current value
        self.excel_time_column_dropdown.set(self.excel_editor.get_excel_time_column_index())
        # bind the event to the excel time column dropdown
        self.excel_time_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_time_column_value(self.excel_time_column_dropdown.get()))

        # create the excel file name column
        self.excel_file_name_column_label = ttk.Label(self.tab2, text='Excel File Name Column')
        # create the excel file name column dropdown
        self.excel_file_name_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel file name column dropdown to the current value
        self.excel_file_name_column_dropdown.set(self.excel_editor.get_excel_file_name_column_index())
        # bind the event to the excel file name column dropdown
        self.excel_file_name_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_file_name_column_value(self.excel_file_name_column_dropdown.get()))

        # create the excel total count column
        self.excel_total_count_column_label = ttk.Label(self.tab2, text='Excel Total Count Column')
        # create the excel total count column dropdown
        self.excel_total_count_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel total count column dropdown to the current value
        self.excel_total_count_column_dropdown.set(self.excel_editor.get_excel_total_count_column_index())
        # bind the event to the excel total count column dropdown
        self.excel_total_count_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_total_count_column_value(self.excel_total_count_column_dropdown.get()))

        # create the save excel column button
        self.save_excel_column_button = ttk.Button(self.tab2, text='Save Excel Column Order', command=self.save_excel_columns)

        # tab 3

        self.excel_name_label = ttk.Label(self.tab3, text='New Excel File Name : ')
        self.excel_name_field= ttk.Entry(self.tab3, textvariable=self.excel_file_name)
        self.excel_name_save_button = ttk.Button(self.tab3, text='Save Excel File Name', command=self.save_excel_file_name)




    def button_dict(self):
        """
        method: button dict
        description: returns a dictionary of the buttons
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
            'excel_total_count_column': self.excel_total_count_column_dropdown
        }

    def load_page(self):
        """
        method: load page
        description: loads the page into the tkinter window
        :return:
        """
        # add the export excel button to the pop up window
        self.export_excel_button.grid(row=1, column=1, pady=15, padx=15)
        # add the load excel by selection button to the pop up window
        self.load_excel_by_selection_button.grid(row=1, column=2, pady=15, padx=15)
        # add the clear predictions button to the pop up window
        self.clear_prediction_data_button.grid(row=2, column=1, pady=15, padx=15)
        # add the clear excel file button to the pop up window
        self.clear_excel_file_button.grid(row=2, column=2, pady=15, padx=15)

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

        self.save_excel_column_button.grid(row=6, column=1, pady=15, padx=15)

        self.excel_name_label.grid(row=0,column=0,pady=15,padx=15)
        self.excel_name_field.grid(row=0,column=1,pady=15,padx=15)
        self.excel_name_save_button.grid(row=0,column=2,pady=15,padx=15)



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
        # split the excel file to check the extension
        split_data = excel_file.split('.')
        # check the extension
        if split_data[-1] != 'xlsx' and split_data[-1] != 'xls' and split_data[-1] != 'csv':
            # if the extension is not .xlsx, .xls, or .csv, show an error
            messagebox.showerror("Incompatible File Extension", f"File must be .xlsx, .xls, or .csv, your file is .{split_data[-1]} ")
            # return the function
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
        self.create_page()
        # create tooltips
        utils.ToolTips(self.button_dict(),'excel_window',2)
        # load the page
        self.load_page()
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
        :return:
        """
        # if the index is 0, resize the tab to 300x200
        if index == 0:
            # resize the tab
            self.geometry('300x200')
        # if the index is 1, resize the tab to 400x400
        elif index == 1:
            # resize the tab
            self.geometry('400x400')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('500x400')

    '''
    
    '''
    def on_tab_change(self):
        """
            method: on tab change
            description: method to resize the tab
        :return:
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
        # set the Excel file variable
        self.excel_file_variable = self.excel_name_field.get()

    def get_excel_file_variable(self):
        return self.excel_file_variable

    def set_excel_file_variable(self, excel_file):
        self.excel_file_variable = excel_file