import tkinter as tk
import tensorflow as tf
from tkinter import PhotoImage # for icons and image graphics
from MainFrame import MainFrame

'''
Paul Yeon's note,
which files have mentions of tooltips as of 2/13/2025:

Utilities.py is this file, which contains the "ToolTips" class 

SettingsWindow.py is a window, like the others it has a button dictionary

MainFrame.py is a window

ExcelWindow.py  is a window

config/tool-tip.json has the blurbs

tooltip.py does each individual tooltip

Most of these files interface with Utilities.py, importing it as utils. 
This function has since been lost due to a much-needed renovation, which though excellent made the replacement buttons 
not have tooltips. If I can keep the same import structure and have the new buttons take the same tooltips

2/20/2025: It looks like the tool-tip.json has the actual words that are used as blurbs for the stuff. 

IT loads in as data alongside a build-in dictionary of buttons and a list of labels
'''

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Devision')
        #self.geometry('1000x1000')
        #self.configure()

        # set minimum window size
        self.minsize(750, 850)

        # set the window icon
        #window_icon = PhotoImage(file = '.\Icons\devision-eye_64x64.png')
        #self.iconphoto(True, window_icon) # if set to 'True', then 'applied to all future created toplevels as well'
        
        ####################################################
        # Check if GPU is available and sends messages to console
        # moved from MainFrame because of newly implemented update display function in MainFrame -skylar
        self.device = '/GPU:0' if tf.config.experimental.list_physical_devices('GPU') else '/CPU:0'
        if self.device == '/GPU:0':
            print(f"Program will use: GPU.")
        else:
            print(f"Program will use: CPU. Warning, processing will be slower as a result. A CUDA compatible NVIDIA GPU is highly recommended.")
        ####################################################
        # Use grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main = MainFrame(self)
        #self.main.geometry(self.main.geometry)
        self.main.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # Run the application
    app = App()
    # Start the event loop
    app.mainloop()
    # commit testing