import tkinter as tk
from tkinter import ttk
from src.WarningWindow import MutImmutable

from PIL.ImageTk import PhotoImage
from PIL import Image


class IdNotFoundError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f'Could not find id {self.value}'

class Page(ttk.Frame):
    id = 0
    def __init__(self,
                 top_frame_kwargs={'padx':5, 'pady':5, 'sticky':'NSEW'},
                 images_frame_kwargs={'padx':5, 'pady':5, 'sticky':'NSEW', 'columnspan':2},
                 image_count=2,
                 *args):
        
        super().__init__(*args)
        
        self.id = Page.id
        Page.id += 1
        
        
        self.top_frame = ttk.Frame(self)
        self.top_frame_iid = 0
        self.top_frame_widgets = {}
        self.top_frame_kwargs = top_frame_kwargs
    
    
        self.settings_frame = ttk.Frame(self)
        self.settings_frame_iid = 0
        self.settings_frame_widgets = {}
        
        
        self.image_pointer = 0
        self.images = []
        self.prediction_images = []
        
        self.images_frame = ttk.Frame(self)
        self.images_frame.left_window = ttk.Label(self, relief='groove')
        self.images_frame.right_window = ttk.Label(self, relief='groove')
        self.images_frame.next_button = ttk.Button(self, text='Next', command=self.next())
        self.images_frame.prev_button = ttk.Button(self, text='Prev', command=self.prev())
        
        self.images_frame.left_window.grid(row=0, column=0, rowspan=4, columnspan=4)
        self.images_frame.right_window.grid(row=0, column=4, rowspan=4, columnspan=4)
        self.images_frame.prev_button.grid(row=4, column=3)
        self.images_frame.next_button.grid(row=4, column=4)
        
        
        self.top_frame.grid(self, row=0, column=0, sticky='NSEW')
        self.images_frame.grid(self, row=1, column=0, sticky='NSEW', rowspan=2)
        self.settings_frame.grid(self, row=3, column=0, sticky='NSEW')
    
    def add_input(self, widget):
        assert isinstance(widget, Inputable)
        widget.master = self.top_frame
        
        iid = self.top_frame_iid
        self.top_frame_iid += 1
        
        self.top_frame_widgets[iid] = widget
        widget.grid(row=0, column=iid, **self.top_frame_kwargs)

    def query_input(self, iid):
        if iid not in self.top_frame_widgets:
            raise IdNotFoundError(iid)
        
        widget = self.top_frame_widgets[iid]
        return widget.input
    
    def add_settings(self, widget):
        assert isinstance(widget, ttk.Frame)
        widget.master = self.settings_frame
        
        iid = self.settings_frame_iid
        self.settings_frame_iid += 1
        
        self.settings_frame[iid] = widget
        widget.pack(side=tk.LEFT, expand=True)

    def next(self):
        self.image_pointer = min(len(self.images), self.image_pointer + 1)
        self.set_image()
        
    def prev(self):
        self.image_pointer = max(0, self.image_pointer - 1)
        self.set_image()
        
    def add_image(self, img):
        self.images.append(img)
        self.prediction_images.append(None)
        
    def set_image(self):
        current_image = self.images[self.image_pointer]
        current_prediction_image = self.prediction_images[self.image_pointer]
        
        self.images_frame.left_window.config(image=current_image)
        
        if current_prediction_image:
            self.images_frame.right_window.config(image=current_prediction_image)
        
        
class Inputable(ttk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.ready_flag = False
        self._input = MutImmutable()
    
    @property
    def input(self):
        if self.ready_flag:
            return self._input['']
        
        else: 
            return None
    
    @input.setter
    def input(self, value):
        self._input[''] = value
        
    def ready(self):
        self.ready_flag = True
        
    def unready(self):
        self.ready_flag = False


# self.subsample_frame = ttk.Frame(self.tab2)
#         self.oyster_slideshow = Slideshow(self, self.tab2)
#         self.subsample_label = ttk.Label(self.subsample_frame, text='Subsample Weight', font=50)
#         self.subsample_weight_field = ttk.Entry(self.subsample_frame, width=5)

#         self.sample_frame = ttk.Frame(self.tab2)
#         self.sample_label = ttk.Label(self.sample_frame, text='Sample Weight', font=50)
#         self.sample_weight_field = ttk.Entry(self.sample_frame, width=5)


#         self.calculate_button = ttk.Button(self.tab2, text='Calculate', command=self.calculate_brood)
#         self.calculated_number = ttk.Label(self.tab2, text='Predicted Sample Number: ', font=50)

#         self.load_oyster_excel_button = ttk.Button(self.tab2, text='Load Oyster Excel', command=self.oyster_page.load_excel_file)
#         self.oyster_export = ttk.Button(self.tab2, text='Export', command=self.oyster_page.run_export_methods)

#         self.oyster_excel_label = ttk.Label(self.tab2, text='No Excel File Selected', font=50)



# self.subsample_frame.grid(row=0, column=0, pady=5, columnspan=1)
#         self.subsample_label.grid(row=0, column=0, pady=5)
#         self.subsample_weight_field.grid(row=1, column=0, pady=5)

#         self.sample_frame.grid(row=0, column=1, pady=5, columnspan=1)
#         self.sample_label.grid(row=0, column=1, pady=5)
#         self.sample_weight_field.grid(row=1, column=1, pady=5)


#         self.calculate_button.grid(row=7, column=0, pady=5)
#         self.calculated_number.grid(row=8, column=0, pady=5)

#         self.load_oyster_excel_button.grid(row=7, column=1, pady=5)
#         self.oyster_excel_label.grid(row=8, column=1, pady=5)
#         self.oyster_export.grid(row=9, column=1, pady=5)