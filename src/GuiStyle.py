from ttkbootstrap import Style
from functools import reduce

    
class StyleSettings():
    def __init__(self):
        # Light theme names set
        self._lt_names = {
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
        }
        
        # Dark theme names set
        self._dt_names = {
            "solar",
            "superhero",
            "darkly",
            "cyborg",
            "vapor"
        }
        
        # Corresponding theme objects as a dictionary
        # Keys are theme names, values are ttkbootstrap.Style objects
        self._themes = reduce(
            lambda x: x.update,
            map(lambda x: {x:Style(theme=x)}, self._dt_names.union(self._lt_names))
        )
    
    @property
    def dt_names(self):
        return self._dt_names
    
    @property
    def lt_names(self):
        return self._lt_names
    
    @property
    def themes(self):
        return self._themes
        
    
    