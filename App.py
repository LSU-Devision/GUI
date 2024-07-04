from MainFrame import MainFrame, Slideshow
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Devision')
        self.geometry('600x600')

        self.main = MainFrame(self)
        self.main.pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()