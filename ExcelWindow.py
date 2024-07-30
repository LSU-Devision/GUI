import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tktooltip import ToolTip

'''
Class: ExcelWindow
Contributors: Alex Mensen-Johnson
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
    
'''
class ExcelWindow(tk.Toplevel):
    def __init__(self, master=None , container=None, excel_editor=None):
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
        self.title('Excel Options')


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
        # add the Basic tab
        self.notebook.add(self.tab1,text="Basic",)
        # add the Advanced tab
        self.notebook.add(self.tab2,text="Advanced")
        # creates the page
        self.run()
    def create_page(self):
        # create the export excel button
        self.export_excel_button = ttk.Button(self.tab1, text='Export Excel', command=self.master.excel_editor.export_predictions_to_excel)
        # create the load excel by selection button
        self.load_excel_by_selection_button = ttk.Button(self.tab1, text='Load Excel', command=self.load_excel_by_selection)
        # create the clear predictions button
        self.clear_prediction_data_button = ttk.Button(self.tab1, text='Clear Predictions',command=self.master.clear_predicted_data)
        # create the clear excel file button
        self.clear_excel_file_button = ttk.Button(self.tab1, text='Clear Excel File', command=self.clear_excel_file)
        # protocol for closing the window
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        # create the excel index column
        self.excel_index_column_toggle = ttk.Button(self.tab2, text='Excel Index Column')
        # create the excel index column dropdown
        self.excel_index_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel index column dropdown to the current value
        self.excel_index_column_dropdown.set(self.excel_editor.get_excel_index_column_index())
        # bind the event to the excel index column dropdown
        self.excel_index_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_index_column_value(self.excel_index_column_dropdown.get()))

        # create the excel date column
        self.excel_date_column_toggle = ttk.Button(self.tab2, text='Excel Date Column')
        # create the excel date column dropdown
        self.excel_date_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel date column dropdown to the current value
        self.excel_date_column_dropdown.set(self.excel_editor.get_excel_date_column_index())
        # bind the event to the excel date column dropdown
        self.excel_date_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_date_column_value(self.excel_date_column_dropdown.get()))

        # create the excel time column
        self.excel_time_column_toggle = ttk.Button(self.tab2, text='Excel Time Column')
        # create the excel time column dropdown
        self.excel_time_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel time column dropdown to the current value
        self.excel_time_column_dropdown.set(self.excel_editor.get_excel_time_column_index())
        # bind the event to the excel time column dropdown
        self.excel_time_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_time_column_value(self.excel_time_column_dropdown.get()))

        # create the excel file name column
        self.excel_file_name_column_toggle = ttk.Button(self.tab2, text='Excel File Name Column')
        # create the excel file name column dropdown
        self.excel_file_name_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel file name column dropdown to the current value
        self.excel_file_name_column_dropdown.set(self.excel_editor.get_excel_file_name_column_index())
        # bind the event to the excel file name column dropdown
        self.excel_file_name_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_file_name_column_value(self.excel_file_name_column_dropdown.get()))

        # create the excel total count column
        self.excel_total_count_column_toggle = ttk.Button(self.tab2, text='Excel Total Count Column')
        # create the excel total count column dropdown
        self.excel_total_count_column_dropdown = ttk.Combobox(self.tab2, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        # set the excel total count column dropdown to the current value
        self.excel_total_count_column_dropdown.set(self.excel_editor.get_excel_total_count_column_index())
        # bind the event to the excel total count column dropdown
        self.excel_total_count_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_excel_total_count_column_value(self.excel_total_count_column_dropdown.get()))

        # create the save excel column button
        self.save_excel_column_button = ttk.Button(self.tab2, text='Save Excel Column', command=self.save_excel_columns)
        # bind the event to the save excel column button
        # self.save_excel_column_button.bind("<Button-1>",lambda event: messagebox.showinfo("Saved", "Excel Column Saved"))

    def create_tooltips(self):
        # time, in s, it takes for the tooltip to appear
        delay = 0.5 

        #create tooltips for each button
        ToolTip(self.export_excel_button, msg="Export predictions to excel", delay=delay)
        ToolTip(self.load_excel_by_selection_button, msg="Choose an excel file to save predictions on", delay=delay)
        ToolTip(self.clear_prediction_data_button, msg="Clear predictions from program", delay=delay)
        ToolTip(self.clear_excel_file_button, msg="Remove loaded excel file", delay=delay)
        #ToolTip(self.excel_index_column_toggle, msg=" ", delay=delay)
        #ToolTip(self.excel_date_column_toggle, msg=" ", delay=delay)
        #ToolTip(self.excel_time_column_toggle, msg=" ", delay=delay)
        #ToolTip(self.excel_file_name_column_toggle, msg=" ", delay=delay)
        #ToolTip(self.excel_total_count_column_toggle, msg=" ", delay=delay)
        #ToolTip(self.save_excel_column_button, msg=" ", delay=delay)
    
    def load_page(self):
        # add the export excel button to the pop up window
        self.export_excel_button.grid(row=1, column=1, pady=15, padx=15)
        # add the load excel by selection button to the pop up window
        self.load_excel_by_selection_button.grid(row=1, column=2, pady=15, padx=15)
        # add the clear predictions button to the pop up window
        self.clear_prediction_data_button.grid(row=2, column=1, pady=15, padx=15)
        # add the clear excel file button to the pop up window
        self.clear_excel_file_button.grid(row=2, column=2, pady=15, padx=15)

        self.excel_index_column_toggle.grid(row=1, column=1, pady=15, padx=15)
        self.excel_index_column_dropdown.grid(row=1, column=2, pady=15, padx=15)

        self.excel_date_column_toggle.grid(row=2, column=1, pady=15, padx=15)
        self.excel_date_column_dropdown.grid(row=2, column=2, pady=15, padx=15)

        self.excel_time_column_toggle.grid(row=3, column=1, pady=15, padx=15)
        self.excel_time_column_dropdown.grid(row=3, column=2, pady=15, padx=15)

        self.excel_file_name_column_toggle.grid(row=4, column=1, pady=15, padx=15)
        self.excel_file_name_column_dropdown.grid(row=4, column=2, pady=15, padx=15)

        self.excel_total_count_column_toggle.grid(row=5, column=1, pady=15, padx=15)
        self.excel_total_count_column_dropdown.grid(row=5, column=2, pady=15, padx=15)

        self.save_excel_column_button.grid(row=6, column=1, pady=15, padx=15)


    '''
    method: clear_excel_file
    description: method to clear the excel file from the program
    '''
    def clear_excel_file(self):
        # clear the excel file from the excel editor
        self.master.excel_editor.set_excel_file(None)
        # clear the excel label
        self.master.excel_editor.set_excel_label(None)
        # set the excel label title to none
        self.master.excel_label_title.config(text='None')
    '''
    method: load_excel_by_selection
    description: method to load the excel file by selection
    '''
    def load_excel_by_selection(self):
        # opens the file dialog to select the excel file
        excel_file = filedialog.askopenfilename(initialdir='/home/max/development/stardist/data')
        # set the excel file in the excel editor
        self.master.excel_editor.set_excel_file(excel_file)
        # create the substring for the excel file
        self.master.excel_editor.get_substring()
        # set the excel label title to the excel file
        self.master.excel_label_title.config(text= str(self.excel_editor.get_excel_label()))
    '''
    method to close the window
    '''
    def close_window(self):
        # close the window
        self.destroy()
        # set the boolean to True to enable a new window
        self.master.is_excel_save_page_open = False
    '''
    method to run the window
    '''
    def run(self):
        # create the page
        self.create_page()
        # create tooltips
        self.create_tooltips()
        # load the page
        self.load_page()
        # sets the boolean to true to prevent duplicates of the window
        self.master.is_excel_save_page_open = True

    def save_excel_columns(self):

        check_list = [self.master.excel_editor.get_excel_index_column_index(),
                      self.master.excel_editor.get_excel_date_column_index(),
                      self.master.excel_editor.get_excel_time_column_index(),
                      self.master.excel_editor.get_excel_file_name_column_index(),
                      self.master.excel_editor.get_excel_total_count_column_index()
                      ]
        check_value = True
        for value in check_list:
            for value2 in check_list[check_list.index(value) + 1:]:
                if value == value2 and value2 != 'None':
                    check_value = False
        if check_value is True:
            self.master.excel_editor.save_excel_settings()
            messagebox.showinfo('Success', 'Excel Columns Saved')
        else:
            messagebox.showerror('Error', 'Excel Columns have the same column value, cannot save')

