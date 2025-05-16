import pandas as pd
from datetime import datetime
from scipy.stats import t
from pathlib import Path
import os

if not os.path.exists('excel'):
    os.mkdir('excel')

def get_csv_path(relative_path):
    """Helper function to get CSV path with environment variable support"""
    if relative_path.startswith('excel/') or relative_path == 'excel':
        path = Path(relative_path)
        subdir = ""
        if os.environ.get('DEVISION_EXCEL'):
            # If we're in a bundled app, use the environment variable path
            if 'excel/' in str(path):
                subdir = str(path).split('excel/', 1)[1]
            path = Path(os.environ.get('DEVISION_EXCEL')) / subdir
            print(f"Using bundled CSV path: {path}")
        
        # Determine if this is a directory or a file path
        if '.' in os.path.basename(path):  # Contains extension, so it's a file
            # Create only the directory part, not the file
            dir_to_create = os.path.dirname(path)
        else:  # It's a directory
            dir_to_create = path
            
        os.makedirs(dir_to_create, exist_ok=True)
        return path
    else:
        # For non-excel paths, still ensure directory exists if it's a file path
        path = Path(relative_path)
        if '.' in os.path.basename(path):  # Contains extension, so it's a file
            os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

class OysterData():
    id = 0
    def __init__(self, *, file_name='oyster-data.csv', staff_name=''):
        self.id = OysterData.id 
        OysterData.id += 1
        
        self.file_name = file_name
        
        formatted_datetime = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        
        # Goes into the info file
        self.info_df = pd.DataFrame([[formatted_datetime, staff_name]], columns=['Date', 'Staff'])
        
        # Goes into the data file
        # Mass is in grams unless otherwise specified
        self.df = pd.DataFrame(columns=[
            'model',
            'group',
            'file-name',
            'size-class',
            'seed-tray-weight', 
            'slide-weight', 
            'slide-and-seed-weight', 
            'subsample-count', 
            'total-number'
        ])
        
        self.data_to_readable = {
            'model':'Model',
            'group':'Group Number',
            'file-name': 'File Name',
            'size-class': 'Size Class',
            'seed-tray-weight': 'Seed Tray Weight (g)',
            'slide-weight': 'Slide Weight (g)',
            'slide-and-seed-weight': 'Slide and Seed Weight (g)',
            'subsample-count': 'Subsample Count',
            'total-number': 'Total Number'}
        
        self.readable_to_data = {self.data_to_readable[k]:k for k in self.data_to_readable}
        
        # Goes into the statistics file
        self.stats = None
        
    def insert(self, *, model, group_number, file_name, size_class,
                        seed_tray_weight, slide_weight,
                        slide_and_seed_weight, subsample_count):
        """Inserts a new value into the OysterData dataframe

        Args:
            model (str): The name of the model used to predict the sample
            group_number (int): The group number of the group being inserted
            file_name (str): The file name where the group count was taken from
            size_class (str): The size class of the group being inserted
            seed_tray_weight (float): The weight of the seed tray used on the group being inserted in grams
            slide_weight (float): The weight of the slide of the group being inserted in grams
            slide_and_seed_weight (float): The weight of the slide and the weight of the seed of the group being inserted in grams
            subsample_count (int): The predicted number of oysters in this sample
        """
        
        
        total_count = (subsample_count / (slide_and_seed_weight - slide_weight)) * seed_tray_weight
        insert_row = pd.DataFrame([[
                str(model),
                int(group_number),
                str(file_name), 
                str(size_class),
                float(seed_tray_weight), 
                float(slide_weight), 
                float(slide_and_seed_weight),
                int(subsample_count),
                int(total_count)
            ]], columns=self.df.columns
        )
        
        
        self.df = pd.concat([self.df, insert_row], ignore_index=True)
        self.compute()
        
    # Takes in a dataframe (of insertable values) and concats it to the current dataframe
    def extend(self, insert_df):
        """Insert all the values in a given dataframe into this objects dataframe

        Args:
            insert_df (pandas.DataFrame): The dataframe being inserted, it must have columns of the same name as this objects dataframe
        """
        
        pd.options.mode.chained_assignment = None

        insert_df = insert_df[['model', 'group', 'file-name', 'size-class', 'seed-tray-weight', 'slide-weight', 'slide-and-seed-weight', 'subsample-count']]
        
        insert_df['group'] = insert_df['group'].astype(int)
        
        total_count = insert_df['subsample-count'] / (insert_df['slide-and-seed-weight'] - insert_df['slide-weight']) * insert_df['seed-tray-weight']
        insert_df['total-number'] = total_count
        
        if len(self.df) == 0: 
            self.df = insert_df
        else:
            self.df = pd.concat([self.df, insert_df], ignore_index=True)
        # Remove duplicate entries by file-name, keeping only the most recent
        self.df = self.df.drop_duplicates(subset=['file-name'], keep='last').reset_index(drop=True)
       
        self.compute()
        pd.options.mode.chained_assignment = 'warn'
        
    def compute(self):
        """Computes mean, standard deviation, standard error, and the deviation of the 95% confidence interval 
           on all groups and saves them into this objects stats attribute as a dataframe
        """
        groups = self.df[['group', 'total-number']].groupby('group')
        
        # Student's T parameters
        dof = groups.size() - 1 # degrees of freedom
        alpha = .05 # also known as p-value
        ppf = t.ppf(1-(alpha/2), dof) # Critical t-value for given degrees of freedom at alpha threshold
        
        # Aggregated statistics
        mean = groups.mean().rename(columns={'total-number':'mean'})
        std = groups.std().rename(columns={'total-number':'std'})
        sem = groups.sem().rename(columns={'total-number':'sem'})
        dof = dof.rename('dof')
        
        confidence95 = sem.apply(lambda x: x*ppf).rename(columns={'sem':'confidence95'})
        
        # Write to dataframe
        self.stats = pd.concat([mean, std, sem, dof, confidence95], axis=1)
    
    def write_csv(self, base_path=None):
        """Writes this object into a single CSV file containing all data entries."""
        # Determine full file path (override if provided) and ensure directory exists
        if base_path:
            file_path = Path(base_path).with_suffix('.csv')
            os.makedirs(file_path.parent, exist_ok=True)
        else:
            file_base = get_csv_path(f'excel/data{self.id}')
            file_path = Path(f"{file_base}.csv")
        
        # Convert data to human-readable columns
        export_df = self.df.copy().rename(columns=self.data_to_readable)
        export_df.index.name = 'Index'
        
        try:
            export_df.to_csv(file_path, index=False)
            print(f"CSV file saved successfully at: {file_path}")
        except Exception as e:
            print(f"Error saving CSV file: {str(e)}")

        try:
            path = file_path.parent / Path(file_path.stem + 'stats' + file_path.suffix)
            self.stats.to_csv(path)
            print(f"Stats csv saved successfully at: {path}")
        except Exception as e:
            print(f"Error saving CSV file: {str(e)}")
            
    # For backward compatibility
    def write_excel(self):
        """Legacy method for backward compatibility"""
        self.write_csv()
    
    def read_csv(self, file_path=None):
        """Reads data from a CSV file
        
        Args:
            file_path: Path to the CSV file to read. If None, uses self.file_name
            
        Returns:
            DataFrame containing the loaded data
        """
        if not file_path:
            file_path = self.file_name
        
        try:
            df = pd.read_csv(file_path)
            df = df.rename(columns=self.readable_to_data)
            
            self.extend(df)
            return df
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return pd.DataFrame()
    
    # For backward compatibility
    def read_excel(self, file_path=None):
        """Legacy method for backward compatibility"""
        return self.read_csv(file_path)

# For backward compatibility
OysterExcel = OysterData

# Testing function
if __name__ == '__main__':  
    import_df = pd.read_csv('test/oyster-example-data.csv')
    data_obj = OysterData(file_name='test/oyster-data-out.csv')
    
    data_obj.extend(import_df)
    data_obj.write_csv()
    
    print(data_obj.read_csv())
    
