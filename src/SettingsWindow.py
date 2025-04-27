import tkinter as tk
from tkinter import ttk, font
from ttkbootstrap import Style
from WarningWindow import WarningWindow

import webbrowser
from Scrapers import Scraper
import json
import pathlib
from os import path
import shutil

from functools import partial

# Window wrapper for settings, ensures that the window is not open when setting are initialized
class Settings(tk.Toplevel):
    instance = None
    is_open = False
    
    def __init__(self, *args, **kwargs):
        if Settings.is_open:
            return
        
        else:
            Settings.is_open = True
            
        super().__init__(*args)
        
        # Make the settings window resizable
        self.resizable(True, True)
        
        # Usually will be mainframe unless the code somehow changes
        self.parent = args[0]
        
        if Settings.instance is None:
            raise AttributeError('No settings instance has been initialized')
            
        self.child = Settings.instance
        self.title('Settings')
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Scale fonts based on screen resolution
        self._scale_fonts(screen_width, screen_height)
        
        # Calculate window size based on screen size (using percentages)
        # Use at most 80% of screen width/height, but not less than minimum values
        width_percentage = 0.35  # 35% of screen width
        height_percentage = 0.6  # 60% of screen height
        
        self.pop_up_window_width = min(max(int(screen_width * width_percentage), 400), 600)
        self.pop_up_window_height = min(max(int(screen_height * height_percentage), 400), 600)
        
        # Position the window - prefer to the right of main window if space allows
        main_window_width = self.parent.winfo_width()
        main_window_height = self.parent.winfo_height()
        main_window_x = self.parent.winfo_rootx()
        main_window_y = self.parent.winfo_rooty()
        
        # First try positioning to the right of main window
        x = main_window_x + main_window_width + 20
        y = main_window_y + (main_window_height // 2 - self.pop_up_window_height // 2)
        
        # If window would be off-screen, center it on screen instead
        if x + self.pop_up_window_width > screen_width:
            x = screen_width // 2 - self.pop_up_window_width // 2
            y = screen_height // 2 - self.pop_up_window_height // 2

        # Set minimum size and geometry
        self.minsize(400, 400)
        self.geometry(f'{self.pop_up_window_width}x{self.pop_up_window_height}+{x}+{y}')
        
        # Placing the child object within the new window
        self.child.create(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.child.grid(row=0, column=0, sticky='nsew')
        
        self.bind('<Destroy>', self.on_destroy)        
    
    def _scale_fonts(self, screen_width, screen_height):
        """Scale fonts based on screen resolution"""
        # Base font sizes for different screen resolutions
        if screen_width >= 2560:  # 4K and higher
            label_size = 11
            default_size = 10
            text_size = 10
        elif screen_width >= 1920:  # Full HD
            label_size = 10
            default_size = 9
            text_size = 9
        else:  # Smaller screens
            label_size = 9
            default_size = 8
            text_size = 8
            
        # Configure font sizes
        font.nametofont("TkHeadingFont").configure(size=label_size)
        font.nametofont("TkDefaultFont").configure(size=default_size)
        font.nametofont("TkTextFont").configure(size=text_size)
    
    def on_destroy(self, event):
        Settings.is_open = False
        
# TODO: Integrate tooltips

class SettingsWindow(ttk.Frame):
    # Class constants
    USER_SETTINGS = path.join('config', 'settings_user.json')
    DEFAULT_SETTINGS = path.join('config', 'settings_default.json')
    USER_THEMES = path.join('config', 'user_themes.json')
    CWD = pathlib.Path.cwd().absolute()
    
    # Initializes before object creation to programmatically create class variables at runtime
    # but before the frame is created
    def __new__(cls, *args):
        # Make sure the config directory exists
        config_dir = path.dirname(cls.DEFAULT_SETTINGS)
        if not path.exists(config_dir):
            try:
                pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error creating config directory: {e}")
                
        if not path.exists(cls.DEFAULT_SETTINGS):
            json_str = """
                        {
                            "toggles":{
                                "excel-default": true,
                                "clear-excel-default" : false,
                                "clear-output-default" : true,
                                "autosave-image-default": true
                            },

                            "theme":"darkly-style"
                        }"""
            try:
                with open(cls.DEFAULT_SETTINGS, 'w') as file:
                    file.write(json_str)
            except Exception as e:
                print(f"Error writing default settings: {e}")
        
        if not path.exists(cls.USER_SETTINGS):
            try:
                shutil.copy(cls.DEFAULT_SETTINGS, cls.USER_SETTINGS)
            except Exception as e:
                print(f"Error copying default settings to user settings: {e}")
             
        try:
            with open(cls.USER_SETTINGS, 'r') as file:
                cls._settings = json.load(file)
        except Exception as e:
            print(f"Error loading user settings: {e}")
            # If we can't load user settings, use default settings
            try:
                with open(cls.DEFAULT_SETTINGS, 'r') as file:
                    cls._settings = json.load(file)
            except Exception as e2:
                print(f"Error loading default settings: {e2}")
                # Fallback to hardcoded settings if everything else fails
                cls._settings = {
                    "toggles": {
                        "excel-default": True,
                        "clear-excel-default": False,
                        "clear-output-default": True,
                        "autosave-image-default": True
                    },
                    "theme": "darkly-style"
                }
        
        # Create USER_THEMES file if it doesn't exist
        if not path.exists(cls.USER_THEMES):
            try:
                with open(cls.USER_THEMES, 'w') as file:
                    file.write('{}')  # Initialize with empty JSON object
            except Exception as e:
                print(f"Error creating user themes file: {e}")
                
        # Load in custom themes from the Style singleton
        try:
            Style().load_user_themes(file=cls.USER_THEMES)
        except Exception as e:
            print(f"Error loading user themes: {e}")
        
        # Intialize the theme from file
        try:
            Style.instance.theme_use(cls._settings['theme'][:-6])
        except Exception as e:
            print(f"Error setting theme: {e}")
        
        try:
            with open(cls.USER_SETTINGS, 'w') as file:
                json.dump(cls._settings, file, indent=2)
        except Exception as e:
            print(f"Error writing user settings: {e}")
        
        # Create a new class object from super method, this also instantiates an object put doesn't call supers init
        return super().__new__(cls)
    
    def __init__(self, *args, **kwargs):
        self.cls = self.__class__
        self.read_only_settings = read_only_settings()
        Settings.instance = self
    
    # Init analogue, runs only when called such that the frame is not created on app startup
    def create(self, *args, **kwargs):
        super().__init__(*args)
        
        # Frame to hold treeview and scrollbars
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # The dropdown menu object with various visual settings
        self._settings_tree = ttk.Treeview(container, columns=("status"), height=30, selectmode='browse')
        
        # Calculate proportional column widths based on window size
        total_width = args[0].pop_up_window_width - 20  # Account for scrollbar and borders
        main_column_width = int(total_width * 0.7)  # 70% for main column
        status_column_width = int(total_width * 0.3)  # 30% for status column
        
        # Set minimum width smaller to accommodate smaller screens
        self._settings_tree.column("#0", width=main_column_width, minwidth=200)
        self._settings_tree.column('status', width=status_column_width, minwidth=100)
        
        self._settings_tree.heading("status", text="Status", anchor="w")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=self._settings_tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self._settings_tree.xview)
        self._settings_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self._settings_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Names for the theme styles
        self.__styles = StyleSettings()
        
        # ids for the various dropdown labels
        header_id = [
            'default',
            'style',    
            'version',
            'clear',            
        ]
        
        # The displayed names for the dropdown labels
        header = [
            'Defaults',
            'Style',
            'Version',
            'Reset/Clear'
        ]
        
        # Put the dropdown labels into the tree
        self._settings_tree.tag_configure("Label", font="TkHeadingFont")
        for id, name in zip(header_id, header): self._settings_tree.insert('', 'end', iid=id, text=name, tags="Label")
        
        # Inititalize the dropdown menu, these methods are separated for readability
        self._default_settings()
        self._style_settings()
        self._version_settings()
        self._clear_settings()
        
        # Initialize the tree from user settings
        self.load_user_settings(SettingsWindow.USER_SETTINGS)
        
        # Make sure the container and treeview expand with the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self._settings_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Add resize handler to adjust column widths when window is resized
        args[0].bind("<Configure>", self._on_window_resize)
    
    def _on_window_resize(self, event):
        """Adjust column widths when window is resized"""
        # Only respond to our parent window's resize events
        if event.widget == self.master:
            # Get current window width
            window_width = event.width
            
            # Recalculate column widths
            total_width = window_width - 20  # Account for scrollbar and borders
            main_column_width = int(total_width * 0.7)
            status_column_width = int(total_width * 0.3)
            
            # Update column widths
            self._settings_tree.column("#0", width=main_column_width)
            self._settings_tree.column('status', width=status_column_width)
    
    # Settings for the default tab
    def _default_settings(self):
        
        # Callback function for turning a toggle from active to inactive and vice versa
        def toggle_setting(event):
            id = self._settings_tree.focus()
            
            # Do not allow the user to automaticly clear if the excel file isn't being automatically created
            if id=='clear-excel-default' and not self.cls._settings['toggles']['excel-default']:
                return
        
            value = 'inactive' if self.cls._settings['toggles'][id] else 'active'
            self._settings_tree.set(id, column='status', value=value)
            self.cls._settings['toggles'][id] = not self.cls._settings['toggles'][id]
            self.write_user_settings()
        
        # More concise, screen-friendly text
        settings_text = [
            "Auto-export Excel file",
            "New Excel for predictions",
            "New Excel when clearing",
            "Auto-save images",
        ]
        
        settings_id = [
            "excel-default",
            "clear-excel-default",
            'clear-output-default',
            'autosave-image-default',
        ]
        
        # Place the default settings into the tree
        for x, id in zip(settings_text, settings_id): 
            self._settings_tree.insert('default', 'end', iid=id, text=x, values='inactive', tags='Toggleable')

        # Bind functions to the inserted settings
        self._settings_tree.tag_configure('Toggleable', font='TkDefaultFont')
        self._settings_tree.tag_bind('Toggleable', '<Return>', toggle_setting)
        self._settings_tree.tag_bind('Toggleable', '<Double-1>', toggle_setting)
        
    def _version_settings(self):
        
        # TODO: Update to github api download methods for security
        # This will require a github api key of some kind
        
        # These are the old SettingsWindow version updater functions
        def update_select(event):
        # create the scraper class
            scraper_class = Scraper()
            # check if there is an internet connection
            if scraper_class.check_internet() is False:
                # if there is no internet connection, show an error
                tk.messagebox.showerror("Error", "No Internet Connection")
                return
            # check if there is a new version
            if scraper_class.check_version() is True:
                # if there is a new version, ask if the user wants to update
                flag = tk.messagebox.askyesno("Update", "There is a new version available. Do you want to update?")
                if flag is True:
                    # open the update page
                    webbrowser.open(scraper_class.get_update_page())
            # if there is no new version show an info box
            else:
                tk.messagebox.showinfo("Update", "You are on the latest version") 
                           
        def guide_select(event):
            scraper_user_guide_class = Scraper()
            # check if there is an internet connection
            if (scraper_user_guide_class.check_internet())  == False:
                # if there is no internet connection, show an error
                tk.messagebox.showerror("Internet Issue", "Fix your internet to the point where you can load google.com")
                return
            # open the user guide page
            else: scraper_user_guide_class.get_user_guide()
            
        
        settings_text = [
           'Check for updates',
           'User guide' 
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
            
            Style.instance.theme_use(theme[:-6])
           
                
            self.write_user_settings()
            
        # Create header for light themes
        self._settings_tree.insert('style', 'end', iid='lt', text="Light Themes", tags="Label")
        # Create header for dark themes
        self._settings_tree.insert('style', 'end', iid='dt', text="Dark Themes", tags="Label")
        
        # Group themes for more compact display - first create light themes
        light_themes_per_row = 3
        for i in range(0, len(self.__styles.lt_names), light_themes_per_row):
            group = self.__styles.lt_names[i:i+light_themes_per_row]
            row_id = f'light_row_{i//light_themes_per_row}'
            
            # For each group, create a row in the tree
            for theme in group:
                # Add individual theme as menu item with proper tag
                self._settings_tree.insert('lt', 'end', iid=theme + '-style', text=theme, tags="Theme", values='inactive')
            
        # Create dark themes rows
        dark_themes_per_row = 3
        for i in range(0, len(self.__styles.dt_names), dark_themes_per_row):
            group = self.__styles.dt_names[i:i+dark_themes_per_row]
            row_id = f'dark_row_{i//dark_themes_per_row}'
            
            # For each group, create a row in the tree
            for theme in group:
                # Add individual theme as menu item with proper tag
                self._settings_tree.insert('dt', 'end', iid=theme + '-style', text=theme, tags="Theme", values='inactive')
        
        self._settings_tree.tag_configure("Theme", font="TkTextFont")
        
        # Bind methods to actions on theme menu types
        # <Double-1> is a double left click, <Return> is the enter key on windows
        self._settings_tree.tag_bind('Theme', '<Double-1>', theme_select)
        self._settings_tree.tag_bind('Theme', '<Return>', theme_select)
        
    def _clear_settings(self):
        def warn_user(command_name, master_func):
            user_yes_no = WarningWindow(self, command_name).wait_for()
            self.bind('<<WarningDone>>', partial(master_func, warn_state=user_yes_no))
        
        # Resets all settings to default
        def reset_select(event):
            warn_user('Reset All Settings', reset_select_yes)
        
        def reset_select_yes(event, warn_state):
            if warn_state['']:
                self.load_user_settings(SettingsWindow.DEFAULT_SETTINGS)
                self.write_user_settings()
            self.unbind_all('<<WarningDone>>')

        
        settings_text = [
            "Reset all settings"
        ]
        
        settings_id = [
            'settings-clear'
        ]
        
        settings_commands = [
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
    
        
    def write_user_settings(self):
        with open(SettingsWindow.USER_SETTINGS, 'w') as file:
            json.dump(self.cls._settings, file, indent=2)
            
  
    
    # # Attribute style getter (pythonic)
    # # This is a read only pointer to the settings
    @property
    def settings(self):
        return self.read_only_settings
    
# Object for storing style names
class StyleSettings():
    def __init__(self):
        # Light theme names set
        self._lt_names = [
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
    
    
# Read only class for distributing settings, updates every time a key is required
# Efficiency can be improved by implementing this as a tree, but irrelevant unless it bottlenecks
# This ensures saftey for the required semi-singleton type of SettingsWindow
# Otherwise works like a dictionary

class read_only_settings():
    def __init__(self, keylist=[]):
        self.keylist = keylist
        self.update()
    
    # Gets the most recent changes to settings
    def update(self):
        # New settings object
        last_item = SettingsWindow._settings
        
        # Traverses down list until it reaches the current dictionary
        for key in self.keylist:
            last_item = last_item[key]
        
        self.__internal_data = last_item
        
        # Turns any dictionaries it finds into read only dictionaries
        for key in self.__internal_data:
            if type(self.__internal_data[key]) == "dict":
                new_keylist = self.keylist.copy()
                new_keylist.append(key)
                self.__internal_data[key] = read_only_settings(new_keylist)
        
    def __getitem__(self, key):
        self.update()
        last_item = self.__internal_data
        for current_key in self.keylist:
            last_item = last_item[current_key]
        return last_item[key]
        
    
    def __len__(self):
        self.update()
        last_item = self.__internal_data
        for current_key in self.keylist:
            last_item = last_item[current_key]
        return len(last_item)
    
    def __repr__(self):
        self.update()
        last_item = self.__internal_data
        for current_key in self.keylist:
            last_item = last_item[current_key]
        return last_item.__repr__()
    
    def __delitem__(self, *args, **kwargs):
        raise TypeError('Cannot delete read-only setting')
    
    def __setitem__(self, *args, **kwargs):
        raise TypeError('Cannot set read-only setting')

        
    