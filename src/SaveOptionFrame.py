from tkinter import ttk
import tkinter as tk 

class SaveOptionFrame(ttk.Frame):
    def __init__(self, *args, kwargs={}, object_name="Empty", type_name="Empty", width=0,
                 button_kwargs={'command':None}, clear_button_kwargs={'command':None}, grid_kwargs={}, label_kwargs={}):
        super().__init__(*args, **kwargs)
        
        self._object_name = object_name
        self._type_name = type_name
        self._column_width = width
        
        self._button = ttk.Button(self, 
                                  text= "Save " + self._type_name, 
                                  **button_kwargs)
        
        self._label = ttk.Label(self, 
                                text=self._object_name, 
                                **label_kwargs)
        
        self._clear_button = ttk.Button(self, 
                                        text="Clear " + self._type_name,
                                        **clear_button_kwargs)
        
        self._button.grid(column=0, row=0, **grid_kwargs)
        self._label.grid(column=1, row=0, **grid_kwargs)
        self._clear_button.grid(column=2, row=0, **grid_kwargs)
        
        for col in range(3):
            self.grid_columnconfigure(col, minsize=self._column_width)
        
    @property
    def title(self):
        return self._type_name + "SaveFrame"