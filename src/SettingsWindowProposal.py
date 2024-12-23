from tkinter import ttk
import tkinter as tk
import json
from src.GuiStyle import StyleSettings
from ttkbootstrap import Style

class Settings(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        self.parent = args[0]
        self.child = kwargs['child']
        
        self.title('Settings')
        self.parent = args[0]
        
        main_window_width = self.parent.winfo_width()
        main_window_height = self.parent.winfo_height()
        
        pop_up_window_width = 600
        pop_up_window_height = 500
        
        x = main_window_width + 75
        y = main_window_height // 2 - pop_up_window_height // 2 

        self.minsize(pop_up_window_width, pop_up_window_height)
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        
        self.child.create(self, parent=self.parent)
        self.child.grid(row=0, column=0, sticky='nsew')
        
        

class SettingsWindow(ttk.Frame):
    USER_SETTINGS = "src/settings_user_proposal.json"
    DEFAULT_SETTINGS = "src/settings_default_proposal.json"
    USER_THEMES = "config/user_themes.json"
    
    def __new__(cls, *args):
        with open(cls.USER_SETTINGS, 'r') as file:
            cls._settings = json.load(file)
            
        Style().load_user_themes(file=cls.USER_THEMES)
        
        try:
            Style(theme=cls._settings['theme'][:-6])
        except AttributeError:
            pass
        
        return super().__new__(cls)
      
    def create(self, *args, **kwargs):
        super().__init__(*args)
        
        
        self.parent = kwargs['parent']
       
        self._settings_tree = ttk.Treeview(self, columns=("status"), height=30, selectmode='browse')
        self._settings_tree.column("#0", width=400, minwidth=250)
        
        self._settings_tree.heading("status", text="Status", anchor="w")
        self.__styles = StyleSettings()
        
        
        header_id = [
            'default',
            'style',    
            'save',
            'version',
            'clear',            
        ]
        
        header = [
            'Defaults',
            'Style',
            'Save',
            'Version',
            'Reset/Clear'
        ]
        
        self._settings_tree.tag_configure("Label", font="TkHeadingFont")
        for id, name in zip(header_id, header): self._settings_tree.insert('', 'end', iid=id, text=name, tags="Label")
        
    
        self._default_settings()
        self._save_settings()
        self._style_settings()
        self._version_settings()
        self._clear_settings()
        
        self.load_user_settings(SettingsWindow.USER_SETTINGS)
        
        self._settings_tree.grid(column=0, row=0, sticky='nsew')
    
    def _default_settings(self):
        
        def toggle_setting(event):        
            id = self._settings_tree.focus()
            value = 'inactive' if SettingsWindow._settings['toggles'][id] else 'active'
            self._settings_tree.set(id, column='status', value=value)
            self._settings['toggles'][id] = not SettingsWindow._settings['toggles'][id]
            self.write_user_settings()
        
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
        
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('default', 'end', iid=id, text=x, values='inactive', tags='Toggleable')
       
        self._settings_tree.tag_configure('Toggleable', font='TkDefaultFont')
        self._settings_tree.tag_bind('Toggleable', '<Return>', toggle_setting)
        self._settings_tree.tag_bind('Toggleable', '<Double-1>', toggle_setting)
        
    
    def _save_settings(self):
        
        #TODO: Fill out these functions
        def model_select(event):
            pass
        def output_select(event):
            pass 
        
        settings_text = [
            "Select default model",
            "Select new output folder"
        ]   
        
        settings_id = [
            'model-save',
            'output-save'
        ] 
        
        settings_commands = [
            model_select,
            output_select
        ]

        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('save', 'end', iid=id, text=x, values='undefined', tags=id)

        for id, func in zip(settings_id, settings_commands):
            self._settings_tree.tag_configure(id, font='TkDefaultFont')
            self._settings_tree.tag_bind(id, '<Return>', func)
            self._settings_tree.tag_bind(id, '<Double-1>', func)
        
    def _version_settings(self):
        
        from SettingsWindow import SettingsWindow
        # TODO: Update these two methods to not use old settings window
        # This will require a github deploy key
        def update_select(event):
            SettingsWindow.check_version(None)
            
        def guide_select(event):
            SettingsWindow.open_user_guide(None)
        
        
        settings_text = [
           'Check for updates',
           'Open user guide' 
        ]
        
        settings_id = [
            'update-version',
            'guide-version'
        ]
        
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('version', 'end', iid=id, text=x, values='command', tags=id)

        self._settings_tree.tag_configure('update-version', font="TkDefaultFont")
        self._settings_tree.tag_configure('guide-version', font="TkDefaultFont")
        
        self._settings_tree.tag_bind('update-version', '<Double-1>', update_select)
        self._settings_tree.tag_bind('update-version', '<Return>', update_select)
        
        self._settings_tree.tag_bind('guide-version', '<Double-1>', guide_select)
        self._settings_tree.tag_bind('guide-version', '<Return>', guide_select)
        
        
    def _style_settings(self):
        
        def theme_select(event):
            theme = self._settings_tree.focus()
            
            self._settings_tree.set(SettingsWindow._settings['theme'], column='status', value='inactive') 
            SettingsWindow._settings['theme'] = theme
            self._settings_tree.set(SettingsWindow._settings['theme'], column='status', value='active')
            
            try:
                Style(theme=theme[:-6])
            except AttributeError:
                pass
                
            self.write_user_settings()
            
        # Create header for light themes
        self._settings_tree.insert('style', 'end', iid='lt', text="Light Themes", tags="Label")
        # Create header for dark themes
        self._settings_tree.insert('style', 'end', iid='dt', text="Dark Themes", tags="Label")
        
        # Fill theme menus
        for x in self.__styles.lt_names: 
            self._settings_tree.insert('lt', 'end', iid= x + '-style', text=x, tags="Theme", values='inactive')
            
        for x in self.__styles.dt_names: 
            self._settings_tree.insert('dt', 'end', iid= x + '-style', text=x, tags="Theme", values='inactive')
        
        self._settings_tree.tag_configure("Theme", font="TkTextFont")
        
        # Bind methods to actions on theme menu types
        # <Double-1> is a double left click, <Return> is the enter key on windows
        self._settings_tree.tag_bind('Theme', '<Double-1>', theme_select)
        self._settings_tree.tag_bind('Theme', '<Return>', theme_select)
        
    def _clear_settings(self):
        
        # TODO: Update these methods for internal clarity
        def model_select(event):
            self.parent.settings.set_model_name(None)
            self.parent.settings.set_model_path(None)
            
        def excel_select(event):
            self.master.settings.set_excel_file_name(None)

        def output_select(event):
            self.parent.excel_editor.set_output_folder('output')
            self.parent.settings.set_output_folder_name('output')
            
        def reset_select(event):
            self.load_user_settings(SettingsWindow.DEFAULT_SETTINGS)
            self.write_user_settings()

        
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
        
        settings_commands = [
            model_select,
            excel_select,
            output_select,
            reset_select
        ]
        
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('clear', 'end', iid=id, text=x, values='command', tags=id)
            
        for id, func in zip(settings_id, settings_commands):
            self._settings_tree.tag_configure(id, font='TkDefaultFont')
            self._settings_tree.tag_bind(id, '<Double-1>', func)
            self._settings_tree.tag_bind(id, '<Return>', func)
        
        
    
    def load_user_settings(self, file_name):
        with open(file_name, 'r') as file:
            SettingsWindow._settings = json.load(file)
        
        for style in self.__styles.lt_names:
            self._settings_tree.set(f'{style}-style', column='status', value='inactive')
        for style in self.__styles.dt_names:
            self._settings_tree.set(f'{style}-style', column='status', value='inactive')
            
        self._settings_tree.set(SettingsWindow._settings['theme'], column='status', value='active')
        
        try:
            Style(theme=SettingsWindow._settings['theme'][:-6])
        except AttributeError:
            pass
        
        for id in SettingsWindow._settings['toggles']:
            value = 'active' if SettingsWindow._settings['toggles'][id] else 'inactive'
            self._settings_tree.set(id, column='status', value=value)
        
            
    def write_user_settings(self):
        with open(SettingsWindow.USER_SETTINGS, 'w') as file:
            json.dump(SettingsWindow._settings, file)
    