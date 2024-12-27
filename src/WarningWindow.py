import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import asyncio

class WarningWindow(tk.Toplevel):
    def __init__(self, frame):
        
            
        def on_destroy(event):
            self.destroy_flag = True
            
        super().__init__()
        #super().__init__(title="Warning!", resizable=(False, False))
        self.title('Warning!')
        self.frame = frame
        
        self.width = self.winfo_screenwidth() // 8
        self.height = self.width
        
        self.minsize(self.width, self.height)
        
        self.frame.create(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='nsew')
        
        self.destroy_flag = False
        self.bind('<Destroy>', on_destroy)
    
    async def button_state(self):
        button_state = False
        while self.destroy_flag != True:
            button_state = await self.frame.button_state()
        
        return button_state
  
        
class WarningFrame(ttk.Frame):
    def __init__(self, dangerous_command_name):
        self.command_name = dangerous_command_name
        self.button_state_bool = None
        self.button_press_flag = False
        self.grid_kwargs = {'padx':25, 'pady':25, 'sticky':'nsew'}

    def create(self, parent):
        def cancel_func(event):
            self.button_state_bool = False
        
        def continue_func(event):
            self.button_state_bool = True
            
        super().__init__(parent)
        
        warning = f"Warning! The command that you are executing ({self.command_name}) cannot be undone!\nDo you wish to proceed?"
        
        self.warning_label = ttk.Label(self, text=warning, font='TkHeadingFont', borderwidth=10, relief='solid', justify='center')
        self.cancel_button = ttk.Button(self, text='Cancel', bootstyle=DANGER, command=cancel_func)
        self.continue_button = ttk.Button(self, text='Continue', bootstyle=SUCCESS, command=continue_func)
                
        self.warning_label.grid(row=0, column=0, columnspan=2, **self.grid_kwargs)
        self.cancel_button.grid(row=1, column=0, **self.grid_kwargs)
        self.continue_button.grid(row=1, column=1, **self.grid_kwargs)

    async def button_state(self):
        while self.button_state_bool == None:
            await asyncio.sleep(.1)
            
        return self.button_state_bool   

   



if __name__ == '__main__':
    root = tk.Tk()
    
    async def main():
        new_frame = WarningFrame('DESTROY EVERYTHING')
        new_window = WarningWindow(new_frame)
        
        
        await get_button_state(new_window)
    
    async def get_button_state(window_obj):
        button_state = await window_obj.button_state()
        print(button_state)
    
    root.minsize(100, 100)
    root.resizable(False, False)
    
    asyncio.run(main())
            
    root.mainloop()
    