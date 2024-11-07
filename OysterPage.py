from tkinter import messagebox, filedialog
import openpyxl
class OysterPage:
    def __init__(self,master):
        self.master = master
        self.prediction_files = master.predictions.prediction_files
        self.excel_file = None
        self.index_row = None
        self.index_row_cells = None
        self.index_row_dict = {}
        self.results_dict = {}

    def calculate(self,sample_weight,subsample_weight,predicted_number):
        subsamples_per_sample = sample_weight / subsample_weight
        predicted_total_count = subsamples_per_sample * predicted_number
        return predicted_total_count

    def oyster_excel_reader(self):
        if self.excel_file is None:
            messagebox.showerror("Error", "Please select an excel file")
            return
        workbook = openpyxl.load_workbook(self.excel_file)
        worksheet = workbook.active
        rows = worksheet.rows
        self.index_row = None
        self.index_row_cells = None
        self.index_row_dict = {}
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


    def get_predicted_values(self):
        if self.master.predictions.predictions_data is not None:
            for prediction in self.master.predictions.predictions_data:
                print(f' Prediction file : {prediction[3]} Predicted Number {prediction[4]}')

    def match_predicted_values(self):
        self.results_dict = {}
        for array in self.index_row_dict['File Names']:
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
        #     print(f'Key is {key} and value is {results_dict[key]}')
        # file_name_row = self.index_row_dict['File Names']
        # for file_name in file_name_row:
        #     print(f'File name is {file_name}')

    def export_data_into_sheet(self):
        pass

    def run_export_methods(self):
        self.oyster_excel_reader()
        self.get_predicted_values()
        self.match_predicted_values()

    def load_excel_file(self):
        self.excel_file = filedialog.askopenfilename(initialdir='/home/max/development/stardist/data')


