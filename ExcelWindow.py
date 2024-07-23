import tkinter as tk
from tkinter import ttk
import Utilities as utils
from tkinter import messagebox

class ExcelWindow(tk.Toplevel):
    def __init__(self, master=None , container=None, excel_editor=None):

        super().__init__(master=master)

        self.master = master

        self.container = container

        self.excel_editor = excel_editor

        main_window_width = self.container.winfo_width()
        # set the size of the pop up window
        main_window_height = self.container.winfo_height()
        # variables for the pop up window
        pop_up_window_width = 300
        # variables for the pop up window
        pop_up_window_height = 200
        # set the position of the pop up window
        x = main_window_width + 75
        # set the position of the pop up window
        y = main_window_height // 2 - pop_up_window_height // 2  # center the pop-up window vertically
        # set the title of the pop up window
        self.title('Excel Options')
        # set the geometry of the pop up window
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')

        if self.excel_editor.get_csv_file() is not None:
            self.excel_editor.get_substring()

        self.run()

    def create_page(self):
        # create the export csv button
        self.export_excel_button = ttk.Button(self, text='Export Excel', command=self.master.export_predictions_to_csv)
        # create the load csv by selection button
        self.load_excel_by_selection_button = ttk.Button(self, text='Load Excel',command=self.master.load_csv_by_selection)
        # create the clear predictions button
        self.clear_prediction_data_button = ttk.Button(self, text='Clear Predictions',command=self.master.clear_predicted_data)
        # create the clear csv file button
        self.clear_excel_file_button = ttk.Button(self, text='Clear Excel File', command=self.master.clear_csv_file)

        #self.protocol("WM_DELETE_WINDOW", lambda: close_window())

        self.excel_index_column_toggle = ttk.Button(self, text='Excel Index Column')
        self.excel_index_column_dropdown = ttk.Combobox(self, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        self.excel_index_column_dropdown.set(self.excel_editor.get_csv_index_column_index())
        self.excel_index_column_dropdown.bind("<<ComboboxSelected>>",lambda event: self.excel_editor.set_csv_index_column_value(self.excel_index_column_dropdown.get()))

        self.excel_date_column_toggle = ttk.Button(self, text='Excel Date Column')
        self.excel_date_column_dropdown = ttk.Combobox(self, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        self.excel_date_column_dropdown.set(self.excel_editor.get_csv_date_column_index())
        self.excel_date_column_dropdown.bind("<<ComboboxSelected>>",lambda event: self.excel_editor.set_csv_date_column_value(self.excel_date_column_dropdown.get()))

        self.excel_time_column_toggle = ttk.Button(self, text='Excel Time Column')
        self.excel_time_column_dropdown = ttk.Combobox(self, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        self.excel_time_column_dropdown.set(self.excel_editor.get_csv_time_column_index())
        self.excel_time_column_dropdown.bind("<<ComboboxSelected>>",lambda event: self.excel_editor.set_csv_time_column_value(self.excel_time_column_dropdown.get()))

        self.excel_file_name_column_toggle = ttk.Button(self, text='Excel File Name Column')
        self.excel_file_name_column_dropdown = ttk.Combobox(self, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        self.excel_file_name_column_dropdown.set(self.excel_editor.get_csv_file_name_column_index())
        self.excel_file_name_column_dropdown.bind("<<ComboboxSelected>>", lambda event: self.excel_editor.set_csv_file_name_column_value(self.excel_file_name_column_dropdown.get()))

        self.excel_total_count_column_toggle = ttk.Button(self, text='Excel Total Count Column')
        self.excel_total_count_column_dropdown = ttk.Combobox(self, state='readonly',values=['None', '1', '2', '3', '4', '5'])
        self.excel_total_count_column_dropdown.set(self.excel_editor.get_csv_total_count_column_index())
        self.excel_total_count_column_dropdown.bind("<<ComboboxSelected>>",lambda event: self.excel_editor.set_csv_total_count_column_value(self.excel_total_count_column_dropdown.get()))

        self.save_excel_column_button = ttk.Button(self, text='Save CSV Column',command=self.excel_editor.save_csv_settings)
        self.save_excel_column_button.bind("<Button-1>",lambda event: messagebox.showinfo("Saved", "Excel Column Saved"))

    def load_page(self):
        # add the export csv button to the pop up window
        self.export_excel_button.grid(row=1, column=1, pady=15, padx=15)
        # add the load csv by selection button to the pop up window
        self.load_excel_by_selection_button.grid(row=1, column=2, pady=15, padx=15)
        # add the clear predictions button to the pop up window
        self.clear_prediction_data_button.grid(row=2, column=1, pady=15, padx=15)
        # add the clear csv file button to the pop up window
        self.clear_excel_file_button.grid(row=2, column=2, pady=15, padx=15)
        '''
        self.window.csv_index_column_toggle.grid(row=1, column=3, pady=15, padx=15)
        self.window.csv_index_column_dropdown.grid(row=1, column=4, pady=15, padx=15)

        self.window.csv_date_column_toggle.grid(row=2, column=3, pady=15, padx=15)
        self.window.csv_date_column_dropdown.grid(row=2, column=4, pady=15, padx=15)

        self.window.csv_time_column_toggle.grid(row=3, column=3, pady=15, padx=15)
        self.window.csv_time_column_dropdown.grid(row=3, column=4, pady=15, padx=15)

        self.window.csv_file_name_column_toggle.grid(row=4, column=3, pady=15, padx=15)
        self.window.csv_file_name_column_dropdown.grid(row=4, column=4, pady=15, padx=15)

        self.window.csv_total_count_column_toggle.grid(row=5, column=3, pady=15, padx=15)
        self.window.csv_total_count_column_dropdown.grid(row=5, column=4, pady=15, padx=15)

        self.window.save_csv_column_button.grid(row=6, column=3, pady=15, padx=15)
        '''

    def run(self):
        # create the page
        self.create_page()
        # load the page
        self.load_page()

