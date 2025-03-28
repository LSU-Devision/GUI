import tkinter as tk
from Pages import OysterPage

if __name__ == '__main__':
    root = tk.Tk()
    frame = OysterPage()
    
    frame.grid(row=0, column=0, sticky='NSEW')
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()