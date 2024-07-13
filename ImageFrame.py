from tkinter import ttk
from PIL import Image, ImageTk

# reworked to maintain aspect ratio in slideshow -skylar
class ImageFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, height=350, width=350, borderwidth=5, relief='sunken')
        self.pack_propagate(0)

        self.image_label = ttk.Label(self)
        self.image_ref = None

        self.image_label.pack()

    def set_image(self, image_path):
        if image_path:
            image = Image.open(image_path)
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height

            if original_width > original_height:
                new_width = 350
                new_height = int(new_width / aspect_ratio)
                if new_height > 350:
                    new_height = 350
                    new_width = int(new_height * aspect_ratio)
            else:
                new_height = 350
                new_width = int(new_height * aspect_ratio)
                if new_width > 350:
                    new_width = 350
                    new_height = int(new_width / aspect_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.image_ref = ImageTk.PhotoImage(image)
        else:
            self.image_ref = None

        self.image_label.config(image=self.image_ref)
        self.image_label.pack(side="top", fill="both", expand="yes")

    def erase_image(self):
        self.image_label.config(image=None)