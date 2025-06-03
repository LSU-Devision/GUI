import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font
import tkinter as tk

class Markdown(ttk.Frame):
    def __init__(self, parent, text: str, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.fonts = {
                "h1": font.Font(size=20, weight="bold"),
                "h2": font.Font(size=16, weight="bold"),
                "h3": font.Font(size=14, weight="bold"),
                "bold": font.Font(weight="bold"),
                "italic": font.Font(slant="italic"),
                "normal": font.Font(size=12)
                }
        
        self.text = ttk.Text(self, wrap=WORD, font=self.fonts['normal'])
        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.text.yview, bootstyle=SECONDARY)
        
        self.text.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        self.define_tags()
        
        self.render_markdown(text)
    
    def define_tags(self):
        self.text.tag_configure("h1", font=self.fonts["h1"], spacing3=10, foreground="#36c")
        self.text.tag_configure("h2", font=self.fonts["h2"], spacing3=8, foreground="#36c")
        self.text.tag_configure("h3", font=self.fonts["h3"], spacing3=6, foreground="#36c")
        self.text.tag_configure("bold", font=self.fonts["bold"])
        self.text.tag_configure("italic", font=self.fonts["italic"])
        self.text.tag_configure("list", lmargin1=25, lmargin2=50)
        self.text.tag_configure("normal", font=self.fonts["normal"])
    
    def render_markdown(self, md: str):
        self.text.delete("1.0", "end")
        lines = md.strip().split('\n')

        for line in lines:
            line = line.rstrip()
            
            if line.startswith("# "):
                self.text.insert("end", line[2:] + "\n", "h1")
            elif line.startswith("## "):
                self.text.insert("end", line[3:] + "\n", "h2")
            elif line.startswith("### "):
                self.text.insert("end", line[4:] + "\n", "h3")
            elif line.startswith("- "):
                self.text.insert("end", u"• " + line[2:] + "\n", "list")
            else:
                self.render_inline(line)
                self.text.insert("end", "\n")

    def render_inline(self, line):
        i = 0
        while i < len(line):
            if line[i:i+2] == "**":
                i += 2
                start = i
                while i < len(line) and line[i:i+2] != "**":
                    i += 1
                self.text.insert("end", line[start:i], "bold")
                i += 2
            elif line[i] == "*":
                i += 1
                start = i
                while i < len(line) and line[i] != "*":
                    i += 1
                self.text.insert("end", line[start:i], "italic")
                i += 1
            else:
                self.text.insert("end", line[i], "normal")
                i += 1
        


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x600")
    
    sample_markdown = \
"""
# Header 1
## Header 2
### Header 3
- List 1
- List 2
**Bold**
*Italic*
Normal
"""
    
    renderer = Markdown(root, sample_markdown)
    renderer.grid()
    
    root.mainloop()