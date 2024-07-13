from tkinter import ttk
from ImageFrame import ImageFrame
import os.path

class Slideshow(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # Copies the image files from the Main frame into the sub frame
        self.image_files = container.image_files
        # Copies the prediction files from the Main frame into the sub frame
        self.prediction_files = container.prediction_files
        # Creates a counter variable called current index
        self.current_index = 0

        self.create_frame()

        self.filepath_label.grid(row=0, column=0, columnspan=2, pady=2)
        self.base_image.grid(row=1, column=0)
        self.predicted_image.grid(row=1, column=1)
        self.item_count_label.grid(row=2, column=0, columnspan=2)
        self.next_image_button.grid(row=3, column=1, padx=2, sticky='w')
        self.prev_image_button.grid(row=3, column=0, padx=2, sticky='e')

    def create_frame(self):
        # Creates a button for next image
        self.next_image_button = ttk.Button(self, text='Next', command=self.next_image)
        # Creates a button for the previous image
        self.prev_image_button = ttk.Button(self, text='Prev', command=self.prev_image)
        # Creates a label for the file path
        self.filepath_label = ttk.Label(self, font=25)
        # Creates an image frame for the base image
        self.base_image = ImageFrame(self)
        # Creates and Image frame for the predicted image
        self.predicted_image = ImageFrame(self)
        # Creates a label for the Item count
        self.item_count_label = ttk.Label(self, font=25)

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
        # concatanates File name with the file name
        new_title = 'Filename: ' + title
        # changes the label to the new title
        self.filepath_label.config(text=new_title)

        prediction_path, num_labels = self.prediction_files.get(image_path, (None, ''))

        self.predicted_image.set_image(prediction_path)
        self.base_image.set_image(image_path)
        
        # adds number predicted to the label
        new_label = 'Number Predicted: ' + str(num_labels)
        # updates tkinter label with the new label
        self.item_count_label.config(text=new_label)