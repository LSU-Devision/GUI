import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
from scipy.stats import t


class OysterExcel():
    def __init__(self, parent=None, *, 
                 file_name='oyster-data.xlsx', staff_name=''):
        # Inherit settings object from parent, this will fail if it is not passed a valid parent object (typically
        # mainframe or one of mainframe's children)
        if parent: self.settings = parent.settings
        
        self.file_name = file_name
        
        formatted_datetime = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        
        # Goes into the info tab
        self.info_df = pd.DataFrame([[formatted_datetime, staff_name]], columns=['Date', 'Staff'])
        
        # Goes into the data tab
        # Mass is in grams unless otherwise specified
        self.df = pd.DataFrame(columns=[
            'group',
            'file-name',
            'size-class',
            'seed-tray-weight', 
            'slide-weight', 
            'slide-and-seed-weight', 
            'subsample-count', 
            'total-number'
        ])
        
        # Goes into the statistics tab
        self.stats = None
        
    def insert(self, *, group_number, file_name, size_class,
                        seed_tray_weight, slide_weight,
                        slide_and_seed_weight, subsample_count):
        
        total_count = (subsample_count / (slide_and_seed_weight - slide_weight)) * seed_tray_weight
        insert_row = pd.DataFrame([[
                group_number,
                file_name, 
                size_class,
                seed_tray_weight, 
                slide_weight, 
                slide_and_seed_weight,
                subsample_count,
                total_count
            ]], columns=self.df.columns
        )
        
        
        self.df = pd.concat([self.df, insert_row], ignore_index=True)
    
    # Takes in a dataframe (of insertable values) sand concats it to the current dataframe
    def extend(self, insert_df):
        total_count = insert_df['subsample-count'] / (insert_df['slide-and-seed-weight'] - insert_df['slide-weight']) * insert_df['seed-tray-weight']
        insert_df['total-number'] = total_count
        
        if len(self.df) == 0: 
            self.df = insert_df
        else:
            self.df = pd.concat([self.df, insert_df], ignore_index=True)
       
    def compute(self):
        groups = self.df[['group', 'total-number']].groupby('group')
        
        # Student's T parameters
        dof = groups.size() - 1 # degrees of freedom
        alpha = .05 # also known as p-value
        ppf = t.ppf(1-(alpha/2), dof) # Critical t-value for given degrees of freedom at alpha threshold

        # Aggregated statistics
        mean = groups.mean().rename(columns={'total-number':'mean'})
        std = groups.std().rename(columns={'total-number':'std'})
        sem = groups.sem().rename(columns={'total-number':'sem'})
        confidence95 = sem.apply(lambda x: x*ppf).rename(columns={'sem':'confidence95'})
        
        # Write to dataframe
        self.stats = pd.concat([mean, std, sem, confidence95], axis=1)
    
    def _openpyxl_write(self, dataframe, workbook, kwargs):
        for row in dataframe_to_rows(dataframe, **kwargs):
            workbook.active.append(row)
            
        for column in workbook.active.columns:
            column_letter = column[0].column_letter
            max_width = len(str(
                max(column, 
                    key = lambda x: len(str(x.value))
                    )
                .value))

            workbook.active.column_dimensions[column_letter].width = max_width + 1
    
    def write_excel(self):
        print_df = self.df.copy()
        print_df = print_df.rename(columns={
            'group':'Group Number',
            'file-name': 'File Name',
            'size-class': 'Size Class',
            'seed-tray-weight': 'Seed Tray Weight (g)',
            'slide-weight': 'Slide Weight (g)',
            'slide-and-seed-weight': 'Slide and Seed Weight (g)',
            'subsample-count': 'Subsample Count',
            'total-number': 'Total Number'
        })
        print_df.index.name = 'Index'
        
        print_stats = self.stats.copy()
        print_stats = print_stats.rename(columns={
            'mean':'Mean',
            'std':'Standard Deviation',
            'sem':'Standard Error',
            'confidence95':'95% Confidence Interval'
        })
        print_stats.index.name = 'Group Number'
        
        wb = Workbook()
        
        info = wb.active
        data = wb.create_sheet(title="Data")
        statistics = wb.create_sheet(title="Statistics")
        
        info.title = "Info"
        
        wb.active = info
        self._openpyxl_write(self.info_df, wb, {'index':False, 'header':True})

        wb.active = data
        self._openpyxl_write(print_df, wb, {'index':True, 'header':True})

        wb.active = statistics
        self._openpyxl_write(print_stats, wb, {'index':True, 'header':True})
        
        wb.save(self.file_name)
            
        

# Testing function
if __name__ == '__main__':  
    import_df = pd.read_csv('test/oyster-example-data.csv')
    excel_obj = OysterExcel(file_name='test/oyster-excel-out.xlsx')
    
    excel_obj.extend(import_df)
    excel_obj.compute()
    
    excel_obj.write_excel()
    
