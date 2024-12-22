from tkinter import ttk
import tkinter as tk
from src.GuiStyle import StyleSettings
from ttkbootstrap import Style

class SettingsWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        self.title('Settings')
        
        main_window_width = args[0].winfo_width()
        main_window_height = args[0].winfo_height()
        
        pop_up_window_width = 300
        pop_up_window_height = 400
        
        x = main_window_width + 75
        y = main_window_height // 2 - pop_up_window_height // 2 
        
        self.minsize(pop_up_window_width, pop_up_window_height)
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        
        
        self._settings_tree = ttk.Treeview(self, height=30, selectmode='browse')
        self._settings_tree.column("#0", width=100, minwidth=50)
        self.__styles = StyleSettings()
        
        header_id = [
            'default',
            'save',
            'load',
            'version',
            'style',
            'clear',            
        ]
        
        header = [
            'Defaults',
            'Save',
            'Load',
            'Version',
            'Style',
            'Clear'
        ]
        
        self._settings_tree.tag_configure("Label", font="TkHeadingFont")
        for id, name in zip(header_id, header): self._settings_tree.insert('', 'end', iid=id, text=name, tags="Label")
        
        
        self._default_settings()
        self._style_settings()
        
        
        self._settings_tree.grid(column=0, row=0, sticky='nsew')
    
    def _default_settings(self):
        settings_text = [
            "Export excel file to output folder upon predicting",
            "Append new predictions to old excel file after predicting",
            "Create new excel file upon clearing images",
            "Automatically save images to output after predicting"
        ]
        
        settings_id = [
            "excel_export",
            "clear_excel",
            'clear_output',
            'autosave_image'
        ]
        
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('default', 'end', iid=id, text=x)
        
        
     
    def _style_settings(self):
        
        def theme_select(event):
            theme = self._settings_tree.focus()[:-5]
            try:
                Style(theme=theme)
            except AttributeError:
                pass
            
        # Create header for light themes
        self._settings_tree.insert('style', 'end', iid='lt', text="Light Themes", tags="Label")
        # Create header for dark themes
        self._settings_tree.insert('style', 'end', iid='dt', text="Dark Themes", tags="Label")
        
        # Fill theme menus
        for x in self.__styles.lt_names: self._settings_tree.insert('lt', 'end', iid= x + 'style', text=x, tags="Theme")
        for x in self.__styles.dt_names: self._settings_tree.insert('dt', 'end', iid= x + 'style', text=x, tags="Theme")
        
        self._settings_tree.tag_configure("Theme", font="TkTextFont")
        
        # Bind methods to actions on theme menu types
        # <Double-1> is a double left click, <Return> is the enter key on windows
        self._settings_tree.tag_bind('Theme', '<Double-1>', theme_select)
        self._settings_tree.tag_bind('Theme', '<Return>', theme_select)
        
    