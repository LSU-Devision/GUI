import pandas as pd
from scipy.stats import t
from src.SettingsWindowProposal import SettingsWindow


class OysterExcel():
    def __init__(self, parent, **kwargs):
        # Inherit settings object from parent, this will fail if it is not passed a valid parent object (typically
        # mainframe or one of mainframe's children)
        self.settings = parent.settings

        # Corresponds to (n) in the oyster excel file
        self.subsample_n = kwargs.get('subsample-n', None)
        
        # Mass is in grams unless otherwise specified
        self.df = pd.DataFrame(columns=['size-class',
                                        'file-name',
                                        'seed-tray-weight', 
                                        'slide-weight', 
                                        'slide-and-seed-weight', 
                                        'subsample-count', 
                                        'total-number'])
        
        self.stats = None
        
    def insert(self, *, file_name, size_class,
                        seed_tray_weight, slide_weight,
                        slide_and_seed_weight, subsample_count):
        
        total_count = (subsample_count / (slide_and_seed_weight - slide_weight)) * seed_tray_weight
        insert_row = pd.DataFrame([[size_class,
                                    file_name, 
                                    seed_tray_weight, 
                                    slide_weight, 
                                    slide_and_seed_weight,
                                    subsample_count,
                                    total_count
                                    ]], columns=self.df.columns)
        
        
        self.df = pd.concat([self.df, insert_row], ignore_index=True)
        
    
    def compute(self):
        groups = self.df.groupby(by = lambda x: x // self.subsample_n).ngroup()
        
        # Student's T parameters
        dof = self.subsample_n - 1 # degrees of freedom
        alpha = .05 # also known as p-value
        ppf = t.ppf(1-(alpha/2), dof) # Critical t-value for given degrees of freedom at alpha threshold
        
        # Aggregated statistics
        mean = groups.mean()
        std = groups.std() # standard deviation
        sem = groups.sem() # standard error
        confidence95 = sem * ppf
                
        self.stats = pd.DataFrame([mean, std, sem, confidence95], columns=['mean', 'std', 'sem', 'dof', 'confidence95'])
    
    
  