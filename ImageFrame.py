from tkinter import ttk
from PIL import Image, ImageTk
class ImageFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, height=200, width=200, borderwidth=5, relief='sunken')
        self.pack_propagate(0)

        self.image_label = ttk.Label(self)
        self.image_ref = None

        self.image_label.pack()

    def set_image(self, image_path):
        if image_path:
            image = Image.open(image_path).resize((200, 200))
            self.image_ref = ImageTk.PhotoImage(image)
        else:
            self.image_ref = None

        self.image_label.config(image=self.image_ref)

    def erase_image(self):
        self.image_label.config(image=None)