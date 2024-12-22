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
        
        pop_up_window_width = 600
        pop_up_window_height = 500
        
        x = main_window_width + 75
        y = main_window_height // 2 - pop_up_window_height // 2 
        
        self.minsize(pop_up_window_width, pop_up_window_height)
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        
        
        self._settings_tree = ttk.Treeview(self, columns=("status"), height=30, selectmode='browse')
        self._settings_tree.column("#0", width=400, minwidth=250)
        
        self._settings_tree.heading("status", text="Status")
        self.__styles = StyleSettings()
        
        header_id = [
            'default',
            'save',
            'version',
            'style',
            'clear',            
        ]
        
        header = [
            'Defaults',
            'Save',
            'Version',
            'Style',
            'Reset/Clear'
        ]
        
        self._settings_tree.tag_configure("Label", font="TkHeadingFont")
        for id, name in zip(header_id, header): self._settings_tree.insert('', 'end', iid=id, text=name, tags="Label")
        
    
        self._default_settings()
        self._save_settings()
        self._version_settings()
        self._style_settings()
        self._clear_settings()
        
        self._settings_tree.grid(column=0, row=0, sticky='nsew')
    
    def _default_settings(self):
        settings_text = [
            "Export Excel file to output folder upon predicting",
            "Append new predictions to old Excel file after predicting",
            "Create new Excel file upon clearing images",
            "Automatically save images to output after predicting"
        ]
        
        settings_id = [
            "excel-default",
            "clear-excel-default",
            'clear-output-default',
            'autosave-image-default'
        ]
        
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('default', 'end', iid=id, text=x)
        
    
    def _save_settings(self):
        settings_text = [
            "Save selected model",
            "Save predictions to Excel",
            "Save current output folder"
        ]   
        
        settings_id = [
            'model-save',
            'excel-save',
            'output-save'
        ] 

        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('save', 'end', iid=id, text=x)

    def _version_settings(self):
        settings_text = [
           'Check for updates',
           'Open user guide' 
        ]
        
        settings_id = [
            'update-version',
            'guide-version'
        ]
        
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('version', 'end', iid=id, text=x)
        
    def _style_settings(self):
        
        def theme_select(event):
            theme = self._settings_tree.focus()[:-6]
            try:
                Style(theme=theme)
            except AttributeError:
                pass
            
        # Create header for light themes
        self._settings_tree.insert('style', 'end', iid='lt', text="Light Themes", tags="Label")
        # Create header for dark themes
        self._settings_tree.insert('style', 'end', iid='dt', text="Dark Themes", tags="Label")
        
        # Fill theme menus
        for x in self.__styles.lt_names: self._settings_tree.insert('lt', 'end', iid= x + '-style', text=x, tags="Theme")
        for x in self.__styles.dt_names: self._settings_tree.insert('dt', 'end', iid= x + '-style', text=x, tags="Theme")
        
        self._settings_tree.tag_configure("Theme", font="TkTextFont")
        
        # Bind methods to actions on theme menu types
        # <Double-1> is a double left click, <Return> is the enter key on windows
        self._settings_tree.tag_bind('Theme', '<Double-1>', theme_select)
        self._settings_tree.tag_bind('Theme', '<Return>', theme_select)
        
    def _clear_settings(self):
        settings_text = [
            "Clear selected model",
            "Clear excel file",
            "Clear output folder",
            "Reset all settings"
        ]
        
        settings_id = [
            'model-clear',
            'excel-clear',
            'output-clear',
            'settings-clear'
        ]
        
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('clear', 'end', iid=id, text=x)
