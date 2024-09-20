import tkinter as tk
import tensorflow as tf
from tkinter import PhotoImage # for icons and image graphics
from MainFrame import MainFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Devision')
        #self.geometry('1000x1000')
        self.configure(bg="#12EFE4")

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