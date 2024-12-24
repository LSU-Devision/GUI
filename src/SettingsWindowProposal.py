import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

import json
import pathlib
from os import path

# Window wrapper for settings, ensures that the window is not open when setting are initialized
class Settings(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        # Usually will be mainframe unless the code somehow changes
        self.parent = args[0]
        
        # The settings window object is passed in as a child to put it in the grid of the new window
        self.child = kwargs['child']
        
        self.title('Settings')
        
        # Pop up windows options
        main_window_width = self.parent.winfo_width()
        main_window_height = self.parent.winfo_height()
        
        pop_up_window_width = 600
        pop_up_window_height = 500
        
        x = main_window_width + 75
        y = main_window_height // 2 - pop_up_window_height // 2 

        self.minsize(pop_up_window_width, pop_up_window_height)
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')
        
        # Placing the child object within the new window
        self.child.create(self, parent=self.parent)
        self.child.grid(row=0, column=0, sticky='nsew')
        
        

class SettingsWindow(ttk.Frame):
    # Class constants
    USER_SETTINGS = path.join('src', 'settings_user_proposal.json')
    DEFAULT_SETTINGS = path.join('src', 'settings_default_proposal.json')
    USER_THEMES = path.join('config', 'user_themes.json')
    USER_HOME = str(pathlib.Path.home())
    
    # Initializes before object creation to programmatically create class variables at runtime
    # but before the frame is created
    def __new__(cls, *args):
        with open(cls.USER_SETTINGS, 'r') as file:
            cls._settings = json.load(file)
        
        # Load in custom themes from the Style singleton
        Style().load_user_themes(file=cls.USER_THEMES)
        
        # Intialize the theme from file
        try:
            Style(theme=cls._settings['theme'][:-6])
        except AttributeError:
            pass
        
        # Create a default output path if not initialized
        if not cls._settings['paths']['output-save']:
            cls._settings['paths']['output-save'] = path.join(cls.USER_HOME, 'output')
            
        # Create a default excel path if not initialized
        if not cls._settings['paths']['excel-save']:
            cls._settings['paths']['excel-save'] = path.join(cls._settings['paths']['output-save'], 'data.xlsx')
        
        with open(cls.USER_SETTINGS, 'w') as file:
            cls._settings = json.dump(cls._settings, file)
        
        # Create a new class object from super method, this also instantiates an object put doesn't call supers init
        return super().__new__(cls)
    
    # Init analogue, runs only when called such that the frame is not created on app startup
    def create(self, *args, **kwargs):
        super().__init__(*args)
        
        self.parent = kwargs['parent']
        self.cls = self.__class__
        
        # The dropdown menu object with various visual settings
        self._settings_tree = ttk.Treeview(self, columns=("status"), height=30, selectmode='browse')
        self._settings_tree.column("#0", width=400, minwidth=250)
        
        self._settings_tree.heading("status", text="Status", anchor="w")
        
        # Names for the theme styles
        self.__styles = StyleSettings()
        
        # ids for the various dropdown labels
        header_id = [
            'default',
            'style',    
            'save',
            'version',
            'clear',            
        ]
        
        # The displayed names for the dropdown labels
        header = [
            'Defaults',
            'Style',
            'File',
            'Version',
            'Reset/Clear'
        ]
        
        # Put the dropdown labels into the tree
        self._settings_tree.tag_configure("Label", font="TkHeadingFont")
        for id, name in zip(header_id, header): self._settings_tree.insert('', 'end', iid=id, text=name, tags="Label")
        
        # Inititalize the dropdown menu, these methods are separated for readability
        self._default_settings()
        self._save_settings()
        self._style_settings()
        self._version_settings()
        self._clear_settings()
        
        # Initialize the tree from user settings
        self.load_user_settings(SettingsWindow.USER_SETTINGS)
        
        # Place the tree
        self._settings_tree.grid(column=0, row=0, sticky='nsew')
    
    # Settings for the default tab
    def _default_settings(self):
        
        # Callback function for turning a toggle from active to inactive and vice versa
        def toggle_setting(event):        
            id = self._settings_tree.focus()
            value = 'inactive' if self.cls._settings['toggles'][id] else 'active'
            self._settings_tree.set(id, column='status', value=value)
            self._settings['toggles'][id] = not self.cls._settings['toggles'][id]
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
        
        # Place the default settings into the tree
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('default', 'end', iid=id, text=x, values='inactive', tags='Toggleable')

        # Bind functions to the inserted settings
        self._settings_tree.tag_configure('Toggleable', font='TkDefaultFont')
        self._settings_tree.tag_bind('Toggleable', '<Return>', toggle_setting)
        self._settings_tree.tag_bind('Toggleable', '<Double-1>', toggle_setting)
        
    
    def _save_settings(self):
        
        # Callback function changing default model filepath and writing to settings
        def model_select(event):
            filename = tk.filedialog.askopenfilename(initialdir = SettingsWindow.USER_HOME, 
                                                     title = "Select a File",
                                                     filetypes=[("Tensorflow Model files", '*.ckpt *.hdf5 *.pb')])
            
            
            self.cls._settings['paths']['model-save'] = filename
            self.write_user_settings() 
        
        # Callback function changing default excel filepath and writing to settings
        def excel_select(event):
            filename = tk.filedialog.askopenfilename(initialdir = SettingsWindow.USER_HOME, 
                                                     title = "Select a File",
                                                     filetypes=[("Excel files", '*.xlsx')])
            
            self.cls._settings['paths']['excel-save'] = filename
            self.write_user_settings()
        
        # Callback function changing default output file directory and writing to settings
        def output_select(event):
            filedirectory = tk.filedialog.askdirectory(initialdir=SettingsWindow.USER_HOME,
                                                       title="Select a File Directory")
            
            self.cls._settings['paths']['output-save'] = filedirectory
            self.write_user_settings()      
            
        settings_text = [
            "Select default model file to import from on startup",
            "Select default excel file to import from on startup",
            "Select an output directory to automatically export data to"
        ]   
        
        settings_id = [
            'model-save',
            'excel-save',
            'output-save'
        ] 
        
        settings_commands = [
            model_select,
            excel_select,
            output_select
        ]

        # Insert settings into tree
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('save', 'end', iid=id, text=x, values='undefined', tags=id)

        # Bind functions onto their respective settings
        for id, func in zip(settings_id, settings_commands):
            self._settings_tree.tag_configure(id, font='TkDefaultFont')
            self._settings_tree.tag_bind(id, '<Return>', func)
            self._settings_tree.tag_bind(id, '<Double-1>', func)
        
    def _version_settings(self):
        # Uses old version settings until we can get an api key
        from SettingsWindow import SettingsWindow as OldSettingsWindow
        # TODO: Update these two methods to not use old settings window
        # This will require a github api key of some kind
        def update_select(event):
            OldSettingsWindow.check_version(None)
            
        def guide_select(event):
            OldSettingsWindow.open_user_guide(None)
        
        
        settings_text = [
           'Check for updates',
           'Open user guide' 
        ]
        
        settings_id = [
            'update-version',
            'guide-version'
        ]
        
        # Insert settings into tree
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('version', 'end', iid=id, text=x, values='command', tags=id)

        # Bind respective functions into tree
        self._settings_tree.tag_configure('update-version', font="TkDefaultFont")
        self._settings_tree.tag_configure('guide-version', font="TkDefaultFont")
        
        self._settings_tree.tag_bind('update-version', '<Double-1>', update_select)
        self._settings_tree.tag_bind('update-version', '<Return>', update_select)
        
        self._settings_tree.tag_bind('guide-version', '<Double-1>', guide_select)
        self._settings_tree.tag_bind('guide-version', '<Return>', guide_select)
        
        
    def _style_settings(self):
        # Callback function for changing style at runtime, writing settings to file
        def theme_select(event):
            theme = self._settings_tree.focus()
            
            self._settings_tree.set(self.cls._settings['theme'], column='status', value='inactive') 
            self.cls._settings['theme'] = theme
            self._settings_tree.set(self.cls._settings['theme'], column='status', value='active')
            
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
        
        # Callback rewrites default model path
        def model_select(event):
            self.cls._settings['paths']['model-save'] = None
            self.write_user_settings()
        
        # Callback rewrites default excel path
        def excel_select(event):
            if not self.cls._settings['paths']['output-save']:
                excel_path = path.join(SettingsWindow.USER_HOME, 'output', 'data.xslx')
            else:
                excel_path = path.join(self.cls._settings['paths']['output-save'], 'data.xlsx')
        
            self.cls._settings['paths']['excel-save'] = excel_path
            self.write_user_settings()
        
        # Callback rewrites defaults output directory
        def output_select(event):
            self.cls._settings['paths']['output-save'] = path.join(SettingsWindow.USER_HOME, 'output')
            self.write_user_settings()
        
        # Resets all settings to default
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
        
        # Place settings in tree
        for x, id in zip(settings_text, settings_id): self._settings_tree.insert('clear', 'end', iid=id, text=x, values='command', tags=id)
            
        # Bind functions to respective settings
        for id, func in zip(settings_id, settings_commands):
            self._settings_tree.tag_configure(id, font='TkDefaultFont')
            self._settings_tree.tag_bind(id, '<Double-1>', func)
            self._settings_tree.tag_bind(id, '<Return>', func)
        
        
    
    def load_user_settings(self, file_name):
        with open(file_name, 'r') as file:
            self.cls._settings = json.load(file)
        
        # Disable all styles
        for style in self.__styles.lt_names:
            self._settings_tree.set(f'{style}-style', column='status', value='inactive')
        for style in self.__styles.dt_names:
            self._settings_tree.set(f'{style}-style', column='status', value='inactive')
        
        # Enable the saved style in the json file
        self._settings_tree.set(self.cls._settings['theme'], column='status', value='active')
        
        try:
            Style(theme=self.cls._settings['theme'][:-6])
        except AttributeError:
            pass
        
        # Read toggleable option states from file and set
        for id in self.cls._settings['toggles']:
            value = 'active' if self.cls._settings['toggles'][id] else 'inactive'
            self._settings_tree.set(id, column='status', value=value)
        
         # Create a default output path if not initialized
        if not self.cls._settings['paths']['output-save']:
            self.cls._settings['paths']['output-save'] = path.join(SettingsWindow.USER_HOME, 'output')
            
        # Create a default excel path if not initialized
        if not self.cls._settings['paths']['excel-save']:
            self.cls._settings['paths']['excel-save'] = path.join(self.cls._settings['paths']['output-save'], 'data.xlsx')
        
        
        # Read paths and set to tree
        for id in self.cls._settings['paths']:
            value = self.cls._settings['paths'][id]
            self._settings_tree.set(id, column='status', value=value)
        
        
    def write_user_settings(self):
        with open(SettingsWindow.USER_SETTINGS, 'w') as file:
            json.dump(self.cls._settings, file)
    
# Object for storing style names
class StyleSettings():
    def __init__(self):
        # Light theme names set
        self._lt_names = [
            "default",
            "cosmo",
            "flatly",
            "journal",
            "litera",
            "lumen",
            "minty",
            "pulse",
            "sandstone",
            "united",
            "yeti",
            "morph",
            "simplex",
            "cerculean"
        ]
        
        # Dark theme names set
        self._dt_names = [
            "solar",
            "superhero",
            "darkly",
            "cyborg",
            "vapor",
            "lsu"
        ]
        
        self._dt_names.sort()
        self._lt_names.sort()

    # Python getters for internal properties
    
    @property
    def dt_names(self):
        return self._dt_names.copy()
    
    @property
    def lt_names(self):
        return self._lt_names.copy()
    
    
    