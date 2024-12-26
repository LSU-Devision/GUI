import pandas as pd
from src.SettingsWindowProposal import SettingsWindow

class OysterExcel():
    def __init__(self, *args, **kwargs):
        # Inherit settings object from parent, this will fail if it is not passed a valid parent object (typically
        # mainframe or one of mainframe's children)
        self.settings = args[0].settings

        # Mass is in grams unless otherwise specified
        self.df = pd.DataFrame(columns=['size-class', 'seed-tray-weight', 'slide-weight', 'slide-and-seed-weight', 'subsample-count', 'total-number', ])
        
        
        
  