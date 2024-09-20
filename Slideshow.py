from tkinter import ttk
from ImageFrame import ImageFrame
import os.path
import Settings

class Slideshow(ttk.Frame):
    def __init__(self, container,container_tab):
        super().__init__(container)
        self.settings = Settings.SettingsJson()
        # Copies the image files from the Main frame into the sub frame
        self.image_files = container.image_files
        # Copies the prediction files from the Main frame into the sub frame
        self.prediction_files = container.prediction_files
        # Creates a counter variable called current index
        self.current_index = 0
        self.container = container_tab
        self.create_frame()
        self.load_frame()


    def load_frame(self):
        self.filepath_label.grid(row=0, column=0, columnspan=2, pady=2)
        self.base_image.grid(row=1, column=0)
        self.predicted_image.grid(row=1, column=1)

        ####################################################
        # Display the predicted image only if the setting is True
        # used in save images output toggle for dynamic display -skylar
        if self.settings.get_save_images_output() == False:
            self.predicted_image.grid_forget()

        self.item_count_label.grid(row=2, column=0, columnspan=2)
        
        ####################################################
        # made previous/next buttons into a frame
        # need to move into own file? -skylar
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row = 3, column = 0, columnspan = 2)
        self.prev_image_button = ttk.Button(self.button_frame, text='Prev', command=self.prev_image)
        self.next_image_button = ttk.Button(self.button_frame, text='Next', command=self.next_image)
        # Pack the buttons with some padding
        self.prev_image_button.pack(side='left', padx=10)
        self.next_image_button.pack(side='left', padx=10)
        # Center the button frame
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=2)
        # end previous/next button frame

    def create_frame(self):
        self.filepath_label = ttk.Label(self, font=50)
        # Creates an image frame for the base image
        self.base_image = ImageFrame(self)
        # Creates and Image frame for the predicted image
        self.predicted_image = ImageFrame(self)
        # Creates a label for the Item count
        self.item_count_label = ttk.Label(self, font=50)
    
    # no longer needed, functionality in main. leaving for now
    # def update_slideshow(self):
    #     #parent_container = self.master
    #     for widget in self.winfo_children():
    #         widget.destroy()
    #     #self.destroy()
    #     self.create_frame()
    #     self.load_frame()
    #     # Re-initialize the frame with the same container
    #     #new_frame = Slideshow(parent_container)

    #     # Add the new frame to the container using grid
    #     #new_frame.grid(row=4, column=0)

    def next_image(self):
        if self.image_files:
            self._to_index(self.current_index + 1)

    def prev_image(self):
        if self.image_files:
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

        prediction_path, num_labels = self.container.predictions.prediction_files.get(image_path, (None, ''))

        self.predicted_image.set_image(prediction_path)
        self.base_image.set_image(image_path)
        
        # adds number predicted to the label
        new_label = 'Number Predicted: ' + str(num_labels)
        # updates tkinter label with the new label
        self.item_count_label.config(text=new_label)