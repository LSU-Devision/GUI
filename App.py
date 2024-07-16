import tkinter as tk
from MainFrame import MainFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Devision')
        #self.geometry('1000x1000')
        self.configure(bg="#12EFE4")

        # set minimum window size
        self.minsize(750, 850)
        
        # Use grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main = MainFrame(self)
        self.main.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # Run the application
    app = App()
    # Start the event loop
    app.mainloop()