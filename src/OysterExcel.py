import pandas as pd
from scipy.stats import t


class OysterExcel():
    def __init__(self, parent=None, **kwargs):
        # Inherit settings object from parent, this will fail if it is not passed a valid parent object (typically
        # mainframe or one of mainframe's children)
        if parent: self.settings = parent.settings

        # Corresponds to (n) in the oyster excel file
        self.subsample_n = kwargs.get('subsample-n', 4)
        
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
        mean = groups.mean()
        std = groups.std() 
        sem = groups.sem()
        confidence95 = sem.apply(lambda x: x*ppf)
        
        # Write to dataframe
        self.stats = pd.concat([mean, std, sem, confidence95], axis=1)
        print(self.stats)
        #self.stats = self.stats.columns = ['mean', 'std', 'sem', 'confidence95']
    
        

# Testing function
if __name__ == '__main__':  
    import_df = pd.read_csv('test/oyster-example-data.csv')
    excel_obj = OysterExcel()
    
    excel_obj.extend(import_df)
    excel_obj.compute()
    
    print(excel_obj.stats)
    print(excel_obj.df)
