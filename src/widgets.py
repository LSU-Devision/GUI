# Motivation for this file:
# Tkinter widget callbacks are very lowlevel (just one step up from pure implementation of asynchronous
# programming with event loops and callbacks). This file creates some widgets with some standard IO operations,
# such as binding one widgets output field to multiple widgets output field (chaining outputs) and creating
# some examples of callback functions that produce a value without having to implement asnychronous pipes/queues

import tkinter.ttk as ttk
import ttkbootstrap
from ttkbootstrap.constants import *
import tkinter as tk
import threading

# This is an object reference to store immutable values, used for carrying variables between callbacks
class MutImmutable():
    def __init__(self, value=None):
        self._val = value

    def __add__(self, value):
        self._val += value
        return self._val
    
    def __radd__(self, value):
        self._val = value + self._val
        return self._val
    
    def __sub__(self, value):
        self._val -= value
        return self._val
    
    def __rsub__(self, value):
        self._value = value - self._value
        return self._val
    
    def __mult__(self, value):
        self._value *= value
        return self._val
    
    def __rmult__(self, value):
        self._value = value * self._value
        return self._val
        
    def __div__(self, value):
        self._value /= value
        return self._val
    
    def __rdiv__(self, value):
        self._value = value / self._value
        return self._val

    def __pow__(self, value):
        self._value **= value
        return self._val
    
    def __floordiv__(self, value):
        self._value //= value
        return self._val
    
    def __repr__(self):
        return repr(self._val)
    
    def __len__(self):
        return len(self._val)
    
    def __setitem__(self, key, val):
        self._val = val
    
    def __getitem__(self, key):
        return self._val
    
    def __str__(self):
        return str(self._val)
    
    def __hash__(self):
        return hash(self._val)
    
class TkIO(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._value = MutImmutable()
    
    #Abstract method
    # I have declined to use the abstract method wrapper as that can potentially run into issues
    # when inheriting from a different super class, as well as requiring a typing module to use
    def pop(self):
        current_input = self._value['']
        self._value[''] = None
        return current_input
    
    #Abstract method
    def push(self, inp):
        self._value[''] = inp

# This class is subclassed by our active widgets
class Tooltips(ttk.Widget):
    def __init__(self, tooltip_string):
        self.tooltip = tooltip_string
    
    def change_tooltip(self, string):
        self.tooltip = string
    
    def display_tooltip(self):
        #This displays a tooltip
        
        #Some functions here
        
        pass
        

class Inputable(TkIO):
    def __init__(self, parent):
        super().__init__(parent)
        self.ready_flag = False
        
    @property
    def value(self):
        if self.ready_flag:
            return self._value['']
        else:
            return None
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
    
    def ready(self):
        self.ready_flag = True
        
    def unready(self):
        self.ready_flag = False
    
    
class Outputable(TkIO):
    def __init__(self, parent):
        super().__init__(parent)
        self.outputs = []
        
    def bind_out(self, io_object, transform=lambda x: x):
        assert isinstance(io_object, Outputable)
        self.outputs.append((io_object, transform))
    
    def bind_to(self, io_object, transform=lambda x: x):
        assert isinstance(io_object, Outputable)
        io_object.outputs.append((self, transform))
    
    @property
    def value(self):
        return self._value['']
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
        self.update()
        
        for (io_obj, transform) in self.outputs:
            out = transform(inp)
            io_obj.value = out
        
    #method to update text, not all widgets will need
    def update(self):
        pass
    
class LabelBox(Inputable):
    def __init__(self, parent, text=''):
        super().__init__(parent)
        
        def text_start(e):
            self.unready()
            
        def text_finish(e):
            self.value = self.box.get()
            self.ready()
                
        self.text = ttk.Label(self, text=text, relief='solid') 
        self.box = ttk.Entry(self, exportselection=0)
        
        self.text.pack(expand=True, fill=tk.BOTH)
        self.box.pack(expand=True, fill=tk.BOTH)
        
        self.box.bind('<FocusIn>', text_start)
        self.box.bind('<FocusOut>', text_finish)

    def pop(self):
        current_text = super().pop()
        self.box.delete(0, tk.END)
        if current_text == None:
            current_text = ''
        return current_text
    
    def push(self, text):
        if text is None:
            text = ''
        
        self.box.delete(0, tk.END)
        self.box.insert(0, text)
        self.value = text
        
class DropdownBox(Inputable):
    def __init__(self, parent, text='', dropdowns=[], command=None):
        super().__init__(parent)
        dropdowns = ['None'] + dropdowns
        
        
        def option_selected(e):
            self.ready()
            self.value = self.menu_var.get()
            
        
        self.text = ttk.Label(self, text=text, relief='solid')
        
        self.menu_var = tk.StringVar(parent, value='None')
        self.menu = ttk.OptionMenu(self, self.menu_var, command=option_selected, *dropdowns)
        
        self.text.pack(expand=True, fill=tk.BOTH)
        self.menu.pack(expand=True, fill=tk.BOTH)
    
    def pop(self):
        current_option = super().pop()
        self.menu_var.set('None')
        self.unready()
        return current_option
    
    def push(self, option):
        if option is None:
            option = 'None'
        
        self.menu_var.set(option)
        self.value = option
        
        if option is not None:
            self.ready()
    
class IOButton(Outputable):
    def __init__(self, parent, command=lambda: None, command_kwargs={}, disable_during_run=False, **kwargs):
        super().__init__(parent)
        
        self.command = command
        self.command_kwargs = command_kwargs
        self.button = ttk.Button(self, command=self.run, **kwargs)
        self.button.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM, anchor=tk.CENTER)
        self.disable=disable_during_run
        
    def run(self):
        def subprocess():
            try:
                if self.disable == True:
                    self.button.config(state='disabled')
                    
                self.value = self.command(**self.command_kwargs)
                
                if self.disable == True:
                    self.button.config(state='normal')
                    
            except Exception as e:
                if self.disable == True:
                    self.button.config(state='normal')
                raise e
                
        threading.Thread(target=subprocess).start()
        
class Counter(Outputable):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        self.text_label = ttk.Label(self, relief='solid', **kwargs)
        self.counter = ttk.Label(self, padding=5, relief='solid', text='-')
        self.text_label.pack(expand=False, side=tk.LEFT, fill=tk.BOTH)
        self.counter.pack(expand=False, side=tk.LEFT, fill=tk.BOTH)
        
    def update(self):
        self.counter.config(text=self.value)
    
    def push(self, inp):
        self.value = inp
        if inp is None:
            self.counter.config(text='-')
            
class ErrorLabel(Outputable):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        self.text_label = ttk.Label(self, relief='solid', foreground='red', font='TkDefaultFont', **kwargs)
        self.text_label.pack(expand=False, side=tk.LEFT, fill=tk.BOTH)
    def update(self):
        self.text_label.config(text=self.value)
    
    def push(self, inp):
        self.value = inp
        if inp is None:
            self.text_label.config(text='')
        else:
            self.text_label.config(text=str(inp))
            
class ProgressBar(Outputable):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        self.progress = ttkbootstrap.Progressbar(self, phase=0, value=100, length=500, bootstyle=SUCCESS)
        self.progress.pack(expand=False, side=tk.LEFT, fill=tk.BOTH)
        
    def update(self):
        if self.value == None or self.value == '':
            self.progress.config(phase=0, value=100)
        else:
            self.progress.config(phase=1, value=self.value)

    def push(self, value):
        self.value = value
        if self.value == None or self.value == '':
            self.progress.config(phase=0, value=100)
        else:
            self.progress.config(phase=1, value=self.value)