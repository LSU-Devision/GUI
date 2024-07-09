from MainFrame import MainFrame
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Devision')
        self.geometry('600x700')
        self.main = MainFrame(self)
        self.main.pack(pady=5)

if __name__ == "__main__":
    # run the application
    app = App()
    # start the event loop
    app.mainloop()