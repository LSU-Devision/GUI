import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.Widgets import MutImmutable

class WarningWindow(tk.Toplevel):
    def __init__(self, parent=None, dangerous_command_name=None):
        """Create a new warning window, button press states can be recieved via .wait_for and binding the 
        '<<WarningDone>>' virtual event to a callback function, see example in __main__ test function for further details

        Args:
            parent (tk.Widget, optional): A reference to the parent object, if given it throws a <<WarningDone>> event to the parent upon completion. Defaults to None.
            dangerous_command_name (str, optional): The name of the command attempting to be run to display to the user. Defaults to None.
        """
        
        # Asynchronous flags and states
        self.button_state = MutImmutable(None)
        self.cancel_flag = True
        self.destroy_flag = True
        self.parent = parent
        if self.parent:
            self.parent_window = parent.winfo_toplevel()
        
        # Callback function to finish up states before destruction
        def on_destroy(event):
            if self.destroy_flag:
                self.destroy_flag = False
                if self.cancel_flag:
                    self.button_state[''] = False
                self._unlock()
                if self.parent:
                    self.parent.event_generate('<<WarningDone>>')
                    
            
            
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
        if self.parent:
            self.parent_window.attributes('-alpha', .5)
    
        
    def _unlock(self):
        """Internal method that unlocks other windows
        """
        self.cancel_flag = False
        self.grab_release()
        if self.parent:
            self.parent_window.attributes('-alpha', 1)
        
    
class WarningFrame(ttk.Frame):
    def __init__(self, dangerous_command_name):
        if dangerous_command_name:
            self.command_name = f"({dangerous_command_name}) "
        else:
            self.command_name = ''
            
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
                
        warning = f"Warning! The command that you are executing {self.command_name} cannot be undone!\nDo you wish to proceed?"
        
        self.warning_label = ttk.Label(self, text=warning, font='TkHeadingFont', borderwidth=10, relief='solid', justify='center')
        self.cancel_button = ttk.Button(self, text='Cancel', bootstyle=DANGER, command=cancel_func)
        self.continue_button = ttk.Button(self, text='Continue', bootstyle=SUCCESS, command=continue_func)
                
        self.warning_label.grid(row=0, column=0, columnspan=2, **self.grid_kwargs)
        self.cancel_button.grid(row=1, column=0, **self.grid_kwargs)
        self.continue_button.grid(row=1, column=1, **self.grid_kwargs)



# Testing function
if __name__ == '__main__':
    root = tk.Tk()
    
    def on_complete(event):
        print(callback_value)
    
    
    callback_value = WarningWindow(parent=root, dangerous_command_name='DESTROY EVERYTHING').wait_for() # A mutable object reference
        
    root.minsize(100, 100)
    root.resizable(False, False)
    
    lbl = ttk.Button(root, text='Luh Button')
    lbl.grid(row=0, column=0)
    
    root.bind('<<WarningDone>>', on_complete) # This virtual event must be bound by the parent
    root.mainloop()
    