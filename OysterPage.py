from tkinter import messagebox, filedialog
import openpyxl
class OysterPage:
    '''
    class: OysterPage
    description: class for the oyster page. currently handles exports and calculations for the oyster page.
    future implementations: modify to create entire oyster Excel file, needs testing and handling for special cases,
        special cases include, mismatching column names, not one to one set of data, not onto data sets, overwriting versus blank data
        also needs to include user warnings for empty data, incorrect file selection, data overwriting.
        far from complete
    modularity: later on, optimize methods for efficiency, certain algorithms have time complexity of n^4. fix this.
    '''
    def __init__(self,master):
        self.master = master
        self.prediction_files = master.predictions.prediction_files
        self.excel_file = None
        #stores the row index of the column headers
        self.index_row = None
        #stores the cells of the index row, i.e the different assigned column values
        self.index_row_cells = None
        #stores the column headers as the key and the cells as the value
        self.index_row_dict = {}
        # stores the row values of the file names as the key and the predicted count as the value
        self.results_dict = {}

    def calculate(self,sample_weight,subsample_weight,predicted_number):
        '''
        method: calculate
        description: calculates the predicted total count from the given user input
        '''
        subsamples_per_sample = sample_weight / subsample_weight
        predicted_total_count = subsamples_per_sample * predicted_number
        return predicted_total_count

    def oyster_excel_reader(self):
        '''
        method: oyster_excel_reader
        description: reads in the excel file, and extracts key values for the program export,\n
        stores the index row value, the index row cells, and the index row dictionary
        '''
        if self.excel_file is None:
            messagebox.showerror("Error", "Please select an excel file")
            return
        workbook = openpyxl.load_workbook(self.excel_file)
        worksheet = workbook.active
        rows = worksheet.rows
        self.index_row = None
        self.index_row_cells = None
        self.index_row_dict = {}
        # for loop has time complexity of n^2, fix this. try index based accessing to make it n
        for row in rows:
            if row[0].value is not None:
                if "Treatment or Group Name" in row[0].value:
                    self.index_row = row[0].row
                    self.index_row_cells = row
                    for cell in self.index_row_cells:
                        column_values = []
                        for col_val in worksheet.iter_rows(min_row=cell.row,min_col=cell.column,max_col=cell.column):
                            column_values.append(col_val)
                        self.index_row_dict[cell.value] = column_values
        workbook.close()


    def get_predicted_values(self):
        '''
        method: get_predicted_values
        description: prints out the predicted values, useful for examining possible errors in the code
        '''
        if self.master.predictions.predictions_data is not None:
            for prediction in self.master.predictions.predictions_data:
                print(f' Prediction file : {prediction[3]} Predicted Number {prediction[4]}')

    def match_predicted_values(self):
        '''
        method: match_predicted_values
        description: matches the predicted values given the existing filenames in the excel file\n
        needs to be tested to see how it handles mismatches between the predicted values and the file names
        '''
        # empties the results dictionary
        self.results_dict = {}
        # Loops through the filenames column to create a dictionary matching row index's to predicted values
        # time complecity is n^3 because of the nested for loops fix this possibly by index based accessing
        for array in self.index_row_dict['File Names']:
            # loops through the array
            for value in array:
                # print(f'File name is {value.value}')
                if value.value is None:
                    continue
                for prediction in self.master.predictions.predictions_data:
                    temp_file_name = value.value.split('\\')[-1].replace('"','')
                    # print(f'Temp file name is {temp_file_name}')
                    # print(f'cell location " {value.column_letter} {value.row}"')
                    if temp_file_name == prediction[3]:
                        # print(f'File name is {temp_file_name} and is matching {prediction[3]},{prediction[4]}')
                        self.results_dict[value.row] = prediction[4]
        # for key in self.results_dict:
        #     print(f'Key is {key} and value is {self.results_dict[key]}')
        # file_name_row = self.index_row_dict['File Names']
        # for file_name in file_name_row:
        #     print(f'File name is {file_name}')

    def export_data_into_sheet(self):
        # open the workbook
        workbook = openpyxl.load_workbook(self.excel_file)
        # set the workbook to the 1st page worksheet
        worksheet = workbook.active
        """
        for key in self.index_row_dict:
            print(key)
        """
        # creates a target column store for accessing the cells by column, result should contain the column of the Subsample count
        target_column = None
        # access the Subsample count column
        # despite nested array, really is n = 2, as noted by the break statements. can be optimized for more efficent access, do later
        for cell_array in self.index_row_dict['Subsample Count']:
            # for loop to access cells to retrieve column letter
            for cell in cell_array:
                target_column = cell.column_letter
                # breaks as for loop is only used once
                break
            # breaks as for loop is only used once
            break
        # uncomment for column checking
        # print(target_column)
        # for loop to write results to dictionary by row
        for key in self.results_dict:
            worksheet[f'{target_column}{key}'] = self.results_dict[key]
        # save the workbook
        workbook.save(self.excel_file)
        # close the workbook.
        workbook.close()


    def run_export_methods(self):
        '''
        method: run_export_methods
        description:modular method, runs the methods to export the data
        '''
        self.oyster_excel_reader()
        self.get_predicted_values()
        self.match_predicted_values()
        self.export_data_into_sheet()
        print('Export complete')

    def load_excel_file(self):
        '''
        method: load_excel_file
        description: loads the excel file from user input
        '''
        self.excel_file = filedialog.askopenfilename(initialdir='/home/max/development/stardist/data')


