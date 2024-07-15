import tkinter as tk
from MainFrame import MainFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Devision')
        self.geometry('1000x1000')
        
        # Configure the grid to make it dynamic
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main = MainFrame(self)
        self.main.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # Run the application
    app = App()
    # Start the event loop
    app.mainloop()
