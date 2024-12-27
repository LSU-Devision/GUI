import tkinter as tk
import tkinter.ttk as tk

class WarningWindow(tk.Toplevel):
    def __init__(self, root):
        self.width = root.winfo_screenwidth()
        

if __name__ == '__main__':
    print('here')
    root = tk.Tk()
    new_window = WarningWindow(root)
    print(new_window.width)
    root.mainloop()