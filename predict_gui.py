import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tensorflow as tf
import os.path
import numpy as np
from csbdeep.utils import normalize
from PIL import Image, ImageTk
from stardist.models import StarDist2D
from tkinter import messagebox

class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.image_files = []
        self.prediction_files = {}

        # Check if GPU is available
        self.device = '/GPU:0' if tf.config.experimental.list_physical_devices('GPU') else '/CPU:0'
        print("Using device:", self.device)

        # Load model on the specified device
        with tf.device(self.device):
            self.model = StarDist2D.from_pretrained('2D_demo')
        
        self.select_files_button = ttk.Button(self, text='Select Files', command=self.select_files)
        self.slideshow = Slideshow(self)

        self.model_select_frame = ttk.Frame(self)
        self.select_model_button = ttk.Button(self.model_select_frame, text='Select Model', command=self.select_model)
        self.model_label = ttk.Label(self.model_select_frame, text='2D_demo')
        self.select_model_button.pack()
        self.model_label.pack()

        self.predict_frame = ttk.Frame(self)
        self.predict_focused_button = ttk.Button(self.predict_frame, text='Predict', command=self.predict_focused)
        self.predict_all_button = ttk.Button(self.predict_frame, text='Predict All', command=self.predict_all)
        self.predict_focused_button.pack()
        self.predict_all_button.pack()
        
        self.select_files_button.grid(row=0, column=0, pady=15)
        self.slideshow.grid(row=1, column=0)
        self.predict_frame.grid(row=2, column=0, pady=15)
        self.model_select_frame.grid(row=3, column=0, pady=15)
        # creates clear button
        self.clear_button = ttk.Button(self,text='Clear Images',command=self.clear_images)
        # adds clear button using grid method
        self.clear_button.grid(row=5, column=0, pady=15)

        # creates a help button that will display button usage
        self.show_info = ttk.Button(self,text='Help Page',command=self.help_page)
        # adds the button to the GUI
        self.show_info.grid(row=6, column=0, pady=15)

    def select_files(self):
        files = filedialog.askopenfilenames(initialdir='/home/max/development/stardist/data')
        self.image_files.extend(files)

        if self.image_files:
            self.slideshow.update_image()

    def select_model(self):
        model_path = filedialog.askdirectory()
        with tf.device(self.device):
            self.model = StarDist2D(None, name=os.path.basename(model_path), basedir=os.path.dirname(model_path))
        self.model_label.config(text=os.path.basename(model_path))

    def _predict(self, image_path):
        img = Image.open(image_path)

        if img.mode != 'L':
            img = img.convert('L')
        
        # Convert the PIL image to a NumPy array
        img = np.array(img)

        # Normalize the image
        img = normalize(img, 1, 99.8, axis=(0,1))

        with tf.device(self.device):
            labels, details = self.model.predict_instances(img)

        save_path = os.path.join('output', 'labels', os.path.basename(image_path))
        save_path = os.path.abspath(save_path)
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        # Convert labels to a PIL image and ensure it's in 'L' mode
        labels_img = Image.fromarray(labels).convert('L')
        labels_img.save(save_path)
        self.prediction_files[image_path] = (save_path, len(details['points']))


    def predict_all(self):
        for image_path in self.image_files:
            self._predict(image_path)

    def predict_focused(self):
        image_path = self.image_files[self.slideshow.current_index]
        self._predict(image_path)
        self.slideshow.update_image()


    '''
    Clear Images: By Alex Mensen-Johnson
    Method for clearing Images from the GUI, resets all variables to their primary state.
    
    '''
    def clear_images(self):
        # Set the base image reference to None
        self.slideshow.base_image.image_ref = None
        # Clear the label of the file path above the slideshow
        self.slideshow.filepath_label.config(text='')
        # Set the index of the pictures to 0
        self.slideshow.current_index = 0
        # empty the image files array
        self.image_files = []
        # set the image to none
        self.slideshow.base_image.set_image(None)
        # set the image files to the current image files, which is none
        self.slideshow.image_files = self.image_files
        # set the predicted image to none
        self.slideshow.predicted_image.set_image(None)
        # set the item count label to empty
        self.slideshow.item_count_label.config(text=' ')

    '''
    Help Page: by Alex Mensen-Johnson
    Description: Loads the Help_Information.txt into a file, reads the file, and displays the information in a pop up
    '''
    def help_page(self):
        # Load File
        info_file = open("Help_Information.txt")
        # Read the file
        file_information = info_file.read()
        # Create the title string
        title = 'Help Page'
        # Create pop up with the information
        messagebox.showinfo(title,file_information)



class ImageFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, height=200, width=200, borderwidth=5, relief='sunken')
        self.pack_propagate(0)

        self.image_label = ttk.Label(self)
        self.image_ref = None

        self.image_label.pack()

    def set_image(self, image_path):
        if image_path:
            image = Image.open(image_path).resize((200,200))
            self.image_ref = ImageTk.PhotoImage(image)
        else:
            self.image_ref = None
        
        self.image_label.config(image=self.image_ref)

    def erase_image(self):
        self.image_label.config(image=None)
        
class Slideshow(ttk.Frame):
    def __init__(self, container): 
        super().__init__(container)

        self.image_files = container.image_files
        self.prediction_files = container.prediction_files
        self.current_index = 0

        self.next_image_button = ttk.Button(self, text='Next', command=self.next_image)
        self.prev_image_button = ttk.Button(self, text='Prev', command=self.prev_image)

        self.filepath_label = ttk.Label(self)

        self.base_image = ImageFrame(self)
        self.predicted_image = ImageFrame(self)

        self.item_count_label = ttk.Label(self)

        self.filepath_label.grid(row=0, column=0, columnspan=2, pady=2)
        self.base_image.grid(row=1, column=0)
        self.predicted_image.grid(row=1, column=1)
        self.item_count_label.grid(row=2, column=0, columnspan=2)
        self.next_image_button.grid(row=3, column=1, padx=2, sticky='w')
        self.prev_image_button.grid(row=3, column=0, padx=2, sticky='e')

    def next_image(self):
        self._to_index(self.current_index + 1)

    def prev_image(self):
        self._to_index(self.current_index - 1)

    def _to_index(self, index):
        self.current_index = index % len(self.image_files)
        self.update_image()

    def update_image(self):
        image_path = self.image_files[self.current_index]

        title = os.path.basename(image_path)
        if len(title) > 20:
            title = title[:10] + '...' + title[-10:]

        self.filepath_label.config(text=title)
        
        prediction_path, num_labels = self.prediction_files.get(image_path, (None, ''))

        self.predicted_image.set_image(prediction_path)
        self.base_image.set_image(image_path)

        self.item_count_label.config(text=num_labels)

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