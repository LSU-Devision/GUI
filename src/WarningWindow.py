import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class WarningWindow(tk.Toplevel):
    def __init__(self, parent=None, dangerous_command_name=''):
        
        # Asynchronous flags and states
        self.button_state = MutImmutable(None)
        self.cancel_flag = True
        self.destroy_flag = True
        
        # Callback function to finish up states before destruction
        def on_destroy(event):
            if self.destroy_flag:
                self.destroy_flag = False
                if self.cancel_flag:
                    self.button_state[''] = False
                self._unlock()
                if parent:
                    parent.event_generate('<<WarningDone>>')
                    
            
            
        super().__init__()
        self.title('Warning!')
        
        # The window contents
        self.frame = WarningFrame(dangerous_command_name=dangerous_command_name)
        
        self.width = self.winfo_screenwidth() // 8
        self.height = self.width
        
        self.minsize(self.width, self.height)
        
        self.frame.create(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='nsew')
        
        self.bind('<Destroy>', on_destroy)
    
    # This method must be called to recieve the mutable object and lock the window
    def wait_for(self):
        """_summary_

        Returns:
            (WarningWindow.MutImmutable): Returns a mutable object reference for immutable datatypes. The immutable value can be queried with any key
        """
        
        self._lock()
        return self.button_state
    
    def _lock(self):
        """Internal method that locks all other windows
        """
        self.cancel_flag = True
        self.grab_set()
        
    def _unlock(self):
        """Internal method that unlocks other windows
        """
        self.cancel_flag = False
        self.grab_release()

    
class WarningFrame(ttk.Frame):
    def __init__(self, dangerous_command_name):
        self.command_name = dangerous_command_name
        self.grid_kwargs = {'padx':25, 'pady':25, 'sticky':'nsew'}

    def create(self, parent): 
        super().__init__(parent)
        
        # Callback functions that represent the cancel and continue state after button press
        def cancel_func():
            parent.button_state[''] = False
            parent._unlock()
            parent.destroy()
        
        def continue_func():
            parent.button_state[''] = True
            parent._unlock()
            parent.destroy()
                
        warning = f"Warning! The command that you are executing ({self.command_name}) cannot be undone!\nDo you wish to proceed?"
        
        self.warning_label = ttk.Label(self, text=warning, font='TkHeadingFont', borderwidth=10, relief='solid', justify='center')
        self.cancel_button = ttk.Button(self, text='Cancel', bootstyle=DANGER, command=cancel_func)
        self.continue_button = ttk.Button(self, text='Continue', bootstyle=SUCCESS, command=continue_func)
                
        self.warning_label.grid(row=0, column=0, columnspan=2, **self.grid_kwargs)
        self.cancel_button.grid(row=1, column=0, **self.grid_kwargs)
        self.continue_button.grid(row=1, column=1, **self.grid_kwargs)

# This is an object reference to store immutable values, used for carrying variables between callbacks
class MutImmutable():
    def __init__(self, value):
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
        return repr(self._value)
    
    def __len__(self):
        return len(self._value)
    
    def __setitem__(self, key, val):
        self._val = val
    
    def __getitem__(self, key):
        return self._val
    
    def __str__(self):
        return str(self._val)



# Testing function
if __name__ == '__main__':
    root = tk.Tk()
    
    def on_complete(event):
        print(callback_value)
    
    
    callback_value = WarningWindow(parent=root, dangerous_command_name='DESTROY EVERYTHING').wait_for()
        
    root.minsize(100, 100)
    root.resizable(False, False)
    lbl = ttk.Button(root, text='Luh Label')
    lbl.grid(row=0, column=0)
    
    root.bind('<<WarningDone>>', on_complete)
    root.mainloop()
    