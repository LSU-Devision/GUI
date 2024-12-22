from ttkbootstrap import Style
import tkinter.ttk as ttk

class StyleFrame(ttk.Frame):
    def __init__(self, *args, kwargs={}):
        # Pass up default frame arguments
        super().__init__(*args, **kwargs)
        
        # Internal title property
        self._title = "Style"
        
        # Internal style dictionary list
        self.__styles = StyleSettings()
        
        # Fill root with frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create treeview for selecting fonts
        self.theme_tree = ttk.Treeview(self, height=7, selectmode="browse")
        # Set size for the column
        self.theme_tree.column("#0", width=100, minwidth=50)
        
        # Create header for light themes
        self.theme_tree.insert('', 'end', 'lt', text="Light Themes", tags=("Label"))
        # Create header for dark themes
        self.theme_tree.insert('', 'end', 'dt', text="Dark Themes", tags=("Label"))
        
        # Fill theme menus
        for x in self.__styles.lt_names: self.theme_tree.insert('lt', 'end', x, text=x, tags=("Theme"))
        for x in self.__styles.dt_names: self.theme_tree.insert('dt', 'end', x, text=x, tags="Theme")
        
        # Configure fonts for distinct menu types
        self.theme_tree.tag_configure("Label", font="TkHeadingFont")
        self.theme_tree.tag_configure("Theme", font="TkTextFont")
        
        # Bind methods to actions on theme menu types
        # <Double-1> is a double left click, <Return> is the enter key on windows
        self.theme_tree.tag_bind('Theme', '<Double-1>', self.select)
        self.theme_tree.tag_bind('Theme', '<Return>', self.select)
        
        # Fill frame with the treeview
        self.theme_tree.grid(row=0, column=0, sticky="nsew")
    
    # Callback method for selecting style type
    def select(self, event):
        theme = self.theme_tree.selection()[0]
        try:
            Style(theme=theme)
        except AttributeError:
            pass
      
    
    # Python getter for title
    @property
    def title(self):
        return self._title
    
# Internal data for theme names for modularity
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
    
    
    