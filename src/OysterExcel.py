import pandas as pd
from src.SettingsWindowProposal import SettingsWindow

class OysterExcel():
    def __init__(self, *args):
        # Inherit settings object from parent, this will fail if it is not passed a valid settings object
        self.settings = args[0].settings
        
        
  