# Motivation for this file:
# Being able to create new image-based pages as easy as building blocks as opposed to hand-coding every single widget
# Pages is specifically for image prediction pages like MainFrame and OysterPage, but the concept is
# able to be generalized

import numpy as np
from csbdeep.utils import normalize
from markdown import Markdown

import datetime
import tkinter as tk
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
import json
from tkinter import ttk

from widgets import *
from settings_window import SettingsWindow, Settings
from oyster_data import OysterExcel
from image_processing import ImageList, THUMBNAIL_SIZE, highlight_boundary

from PIL.ImageTk import PhotoImage, getimage
from PIL import Image

import os
from pathlib import Path

import pandas as pd

from model import ModelAPI

import tempfile
import cv2
import sys

# Raspberry Pi detection and picamera2 import check
def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read().lower()
        if any(x in cpuinfo for x in ['raspberry pi', 'bcm2708', 'bcm2709', 'bcm2710', 'bcm2711', 'bcm2712']):
            return True
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as f:
                model = f.read()
                if 'raspberry pi' in model.lower():
                    return True
        except:
            pass
        try:
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read()
                if 'raspberry pi' in model.lower():
                    return True
        except:
            pass
        return False
    except:
        return False

def has_picamera2():
    try:
        import picamera2 # type: ignore
        return True
    except ImportError:
        return False

INTIAL_DIR = Path.cwd()


class IdNotFoundError(Exception):
    def __init__(self, value):
        """Create a new exception for invalid Ids

        Args:
            value (object): id object
        """
        self.value = value
        
    def __repr__(self):
        return f'Could not find id {self.value}'

# A frame subclass that is meant to modularize the image-frame predictor setup, allowing for any image annotatation 
# and prediction instance be easily replicated

class Page(ttk.Frame):
    # Static variables
    id = 0
    black_image = Image.new(mode='RGB', color=(0, 0, 0), size=THUMBNAIL_SIZE)    
    
    
    def __init__(self,
                 *args,
                 **kwargs):
        
        # Key word arguements to pass into the grid function of respective subframes of Page
        if 'top_frame_kwargs' not in kwargs:
            top_frame_kwargs={'padx':5, 'pady':5, 'sticky':'NS'}
        if 'settings_frame_kwargs' not in kwargs:
            settings_frame_kwargs={'sticky':'EW', 'padx':10}
        if 'output_frame_kwargs' not in kwargs:
            output_frame_kwargs={'sticky':'EW', 'padx':10}
        
        # Initializing ttk widget methods in ttk.Frame
        super().__init__(*args)
        
        # Creating a unique identifier for different pages
        self.id = Page.id
        Page.id += 1
        
        if not hasattr(self, 'name'):
            self.name = f"Page{self.id}"
        
        # Default display for empty image frames so that the frame will be sized appropriately
        self.black_photoimage = PhotoImage(Page.black_image)

        # Below are attributes that keep track of the various save states of widgets on subframes
        self.file_name_dict = {}
        
        self.top_frame = ttk.Frame(self)
        self.top_frame_iid = 0
        self.top_frame_widgets = {}
        self.top_frame_kwargs = top_frame_kwargs
        self.top_frame_saves = {}

        self.output_frame = ttk.Frame(self)
        self.output_frame_iid = 0
        self.output_frame_widgets = {}
        self.output_frame_kwargs = output_frame_kwargs
        self.output_frame_saves = {}
        
        self.settings_frame = ttk.Frame(self)
        self.settings_frame_iid = 0
        self.settings_frame_widgets = {}
        self.settings_frame_kwargs = settings_frame_kwargs
        
        # Grid styling options, giving more weight to the image subframes
        # Set minsize and weights for all rows to prevent overlap and hiding
        self.rowconfigure(0, weight=3, minsize=60)   # top_frame
        self.rowconfigure(1, weight=2, minsize=200)  # images_frame
        self.rowconfigure(2, weight=3, minsize=60)   # output_frame
        self.rowconfigure(3, weight=3, minsize=60)   # settings_frame
        for column in range(0,1):
            self.columnconfigure(column, weight=1)
        
        self.image_pointer = 0
        
        # Reading and writing image data from file
        
        true_json = [] 
        pred_json = []
        if os.path.exists(f'data/ImageListTrue{self.name}.json'):
            with open(f'data/ImageListTrue{self.name}.json', 'r') as file:
                true_json = list(json.load(file))
        if os.path.exists(f'data/ImageListPred{self.name}.json'):
            with open(f'data/ImageListPred{self.name}.json', 'r') as file:
                pred_json = list(json.load(file))
        self.images = ImageList(iterable=true_json, name=f'True{self.name}')
        self.prediction_images = ImageList(iterable=pred_json, name=f'Pred{self.name}')
        
        # Store original PIL images for resizing
        self._original_images = []
        self._original_pred_images = []
        # Manual setup for images frame
        self.images_frame = ttk.Frame(self)
        self.images_frame_kwargs = {
            'padx':5,
            'pady':10
        }
        # --- Button frame for centering image buttons ---
        self.images_frame.button_frame = ttk.Frame(self.images_frame)
        self.images_frame.button_frame.grid(row=0, column=0, columnspan=3, sticky='EW', **self.images_frame_kwargs)
        self.images_frame.button_frame.columnconfigure(0, weight=1)
        self.images_frame.button_frame.columnconfigure(1, weight=1)
        # Create buttons with same width
        button_width = 20
        self.images_frame.file_select = ttk.Button(self.images_frame.button_frame, text='Select an image', command=self.add_image, style='Image.TButton', width=button_width)
        self.images_frame.take_image = ttk.Button(self.images_frame.button_frame, text='Take an image', command=self.take_image, style='Image.TButton', width=button_width)
        
        if is_raspberry_pi():
            self.images_frame.take_image.grid(row=0, column=1, padx=5, pady=0, sticky='EW')
            self.images_frame.file_select.grid(row=0, column=0, padx=5, pady=0, sticky='EW')

        else:
            self.images_frame.file_select.grid(row=0, column=0, columnspan=2, padx=5, pady=0, sticky='EW')
        # --- End button frame ---
        # Set fixed size for image display labels
        self.images_frame.left_window = tk.Label(
            self.images_frame,
            relief='groove',
            image=self.black_photoimage,
            width=THUMBNAIL_SIZE[0],
            height=THUMBNAIL_SIZE[1]
        )
        self.images_frame.right_window = tk.Label(
            self.images_frame,
            relief='groove',
            image=self.black_photoimage,
            width=THUMBNAIL_SIZE[0],
            height=THUMBNAIL_SIZE[1]
        )
        # Add fullscreen buttons for left and right images
        self.images_frame.left_fullscreen_btn = ttk.Button(
            self.images_frame, text='⛶', width=2, command=lambda: self.show_fullscreen_image('left'))
        self.images_frame.right_fullscreen_btn = ttk.Button(
            self.images_frame, text='⛶', width=2, command=lambda: self.show_fullscreen_image('right'))
        # Place fullscreen buttons near the image labels (top-right corner of each image label)
        self.images_frame.left_window.grid(row=1, column=0, rowspan=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.left_fullscreen_btn.grid(row=1, column=0, sticky='ne', padx=8, pady=8)
        self.images_frame.right_window.grid(row=1, column=2, rowspan=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.right_fullscreen_btn.grid(row=1, column=2, sticky='ne', padx=8, pady=8)
        self.images_frame.next_button = ttk.Button(self.images_frame, text='Next', command=self.next)
        self.images_frame.prev_button = ttk.Button(self.images_frame, text='Prev', command=self.prev)
        self.images_frame.counter = ttk.Label(self.images_frame, text='-/0', relief='groove', anchor='center')
        self.images_frame.clear_images = ttk.Button(self.images_frame, text='Clear all images', command=self.clear_all_images)
        self.images_frame.left_window.grid(row=1, column=0, rowspan=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.right_window.grid(row=1, column=2, rowspan=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.prev_button.grid(row=3, column=0, sticky='', **self.images_frame_kwargs)
        self.images_frame.next_button.grid(row=3, column=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.counter.grid(row=3, column=1, sticky='EW', **self.images_frame_kwargs)
        self.images_frame.clear_images.grid(row=2, column=1, stick='EW', **self.images_frame_kwargs)
        for row in [0,3]:
            self.images_frame.rowconfigure(row, weight=1, minsize=50)
        for row in [1, 2]:
            self.images_frame.rowconfigure(row, weight=2, minsize=50 if row == 2 else 0)
        self.images_frame.columnconfigure(0, weight=1)
        self.images_frame.columnconfigure(2, weight=1)
        # Bind resize event to images_frame
        self.images_frame.bind('<Configure>', self._on_images_frame_resize)
        
        # Placing the frames onto the page
        
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.images_frame.grid(row=1, column=0, sticky='NSEW')
        self.output_frame.grid(row=2, column=0, sticky='NSEW')
        self.settings_frame.grid(row=3, column=0, sticky='NSEW')
        
        self.settings_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)
            
        # Writing images read from disk onto frame in order, if applicable
        for index in range(len(self.images)):
            file_path = self.images.paths[index]
            with Image.open(file_path) as og_img:
                self._original_images.append(og_img.copy())
            
            # Reload prediction images    
            file_path_pred = self.prediction_images.paths[index]
            try:
                with Image.open(file_path_pred) as og_pred_img:
                    self._original_pred_images.append(og_pred_img.copy())
            except:
                self._original_pred_images.append(None)
            self.file_name_dict[index] = file_path
            self.next()
        
    def disable_move_buttons(self):
        self.images_frame.next_button.config(state='disabled')
        self.images_frame.prev_button.config(state='disabled')
        self.images_frame.file_select.config(state='disabled')
        self.images_frame.clear_images.config(state='disabled')     
    
    def enable_move_buttons(self):
        self.images_frame.next_button.config(state='enabled')
        self.images_frame.prev_button.config(state='enabled')
        self.images_frame.file_select.config(state='enabled')
        self.images_frame.clear_images.config(state='enabled')
        
    def add_input(self, widget, **kwargs):
        """Adds and manages a subclass of Inputable onto the top frame, these
        are meant to contain widgets that recieve inputs

        Args:
            widget (Inputable (Class)): An uninstantiated widget class
            kwargs: Keyword arguments for the widget being instantiated
        Returns:
            Inputable (Object): A pointer to the instantiated widget object  
        """
        assert issubclass(widget, Inputable)
        widget = widget(self.top_frame, **kwargs)
        
        iid = self.top_frame_iid
        self.top_frame_iid += 1
        
        self.top_frame_widgets[iid] = widget
        self.top_frame.columnconfigure(iid, weight=1)
        
        widget.grid(row=0, column=iid, **self.top_frame_kwargs)
        return widget

    def query_input(self, iid):
        """Returns the value of an inputable widget based on its integer id,
        widgets are given ids based on the order they were called in

        Args:
            iid (int): The integer id of the inputable widget on top frame

        Raises:
            IdNotFoundError: If there doesn't exist a widget with the integer id specified, an IdNotFoundError is raised

        Returns:
            MutImmutable: The value contained in widget
        """
        if iid not in self.top_frame_widgets:
            raise IdNotFoundError(iid)
        
        widget = self.top_frame_widgets[iid]
        return widget.value
    
    def get_frame_inputs(self):
        """Dataframe compatible version of all data stored in the top frame in the current image

        Returns:
            dict: Dictionary in dataframe format containing all top frame widget data from this image
        """
        return {self.image_pointer:{iid:self.top_frame_widgets[iid].value for iid in self.top_frame_widgets}}   
    
    def get_all_inputs(self):
        """Dataframe compatible version of all data stored in the top frame across all images

        Returns:
            dict: Dictionary in dataframe format containing all top frame widget data from all images
        """
        if len(self.images) == 0:
            return {}
        
        self.save_frame()

        data = {}
        for img_pointer in range(len(self.images)):
            if img_pointer not in self.top_frame_saves:
                data[img_pointer] = {iid:None for iid in self.top_frame_widgets}
            else:
                data[img_pointer] = {k:v for k, v in self.top_frame_saves[img_pointer]}
                
        self.write_frame()
        return data
    
    def save_frame(self):
        """Saves all the current data into a dictionary
        """
        top_widgets = tuple(self.top_frame_widgets.keys())
        top_widget_data = tuple(map(lambda x: self.top_frame_widgets[x].pop(), top_widgets))
        self.top_frame_saves[self.image_pointer] = tuple(zip(top_widgets, top_widget_data))
        
        out_widgets = tuple(self.output_frame_widgets.keys())
        out_widget_data = tuple(map(lambda x: self.output_frame_widgets[x].pop(), out_widgets))
        self.output_frame_saves[self.image_pointer] = tuple(zip(out_widgets, out_widget_data))
        
    def write_frame(self):
        """Writes data from saved dictionaries to frame based on the current image selected
        """
        if self.image_pointer not in self.top_frame_saves:
            for iid in self.top_frame_widgets:
                self.top_frame_widgets[iid].push(None)
            for iid in self.output_frame_widgets:
                self.output_frame_widgets[iid].push(None)
            return
        
        widget_data = self.top_frame_saves[self.image_pointer]
        for widget in widget_data:
            self.top_frame_widgets[widget[0]].push(widget[1])
        
        widget_data = self.output_frame_saves[self.image_pointer]
        for widget in widget_data:
            self.output_frame_widgets[widget[0]].push(widget[1])
        
    def add_settings(self, widget, **kwargs):
        """_summary_

        Args:
            widget (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert issubclass(widget, ttk.Widget)
        widget = widget(self.settings_frame, **kwargs)
                
        iid = self.settings_frame_iid
        self.settings_frame_iid += 1
        
        self.settings_frame_widgets[iid] = widget
        self.settings_frame.columnconfigure(iid, weight=1)

        widget.grid(row=0, column=iid, **self.settings_frame_kwargs)
        return widget

    def add_output(self, widget, **kwargs):
        """_summary_

        Args:
            widget (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert issubclass(widget, Outputable)
        widget = widget(self.output_frame, **kwargs)
        
        iid = self.output_frame_iid
        self.output_frame_iid += 1
        
        self.output_frame_widgets[iid] = widget
        self.output_frame.columnconfigure(iid, weight=1)
        
        widget.grid(row=0, column=iid, **self.output_frame_kwargs)
        return widget
    
    def next(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if len(self.images) == 0:
            return None
        
        self.save_frame()
        self.image_pointer = min(len(self.images)-1, self.image_pointer + 1)
        self.write_frame()

        self.set_image()
        
    def prev(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if len(self.images) == 0:
            return None
        
        self.save_frame()
        self.image_pointer = max(0, self.image_pointer - 1)
        self.write_frame()
        
        self.set_image()
    
    def add_image(self):
        """Allow selecting and uploading multiple images at once."""
        initialdir = get_images_path('images')
        # Always ensure the directory exists
        try:
            os.makedirs(initialdir, exist_ok=True)
            print(f"Ensured images directory exists: {initialdir}")
        except Exception as e:
            print(f"Warning: Could not create images directory: {str(e)}")
        
        from tkinter.filedialog import askopenfilenames
        file_paths = askopenfilenames(
            initialdir=initialdir,
            title='Please select image(s)',
            filetypes=[('Images', '*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG *.tif *.TIF')]
        )
        if not file_paths:
            return
        last_file_path = None
        for file_path in file_paths:
            if Path(file_path).suffix not in ['.jpg', '.JPG', '.jpeg', '.png', '.PNG', '.tif', '.TIF']:
                continue
            # Store original PIL image
            pil_img = Image.open(file_path)
            self._original_images.append(pil_img.copy())
            pil_img.close()
            self.images.append(file_path)
            self.prediction_images.append(None)
            self._original_pred_images.append(None)
            self.update_image(file_path)
            last_file_path = file_path
        # Only update the UI to the last image added
        if last_file_path:
            self.set_image()
        
    def update_image(self, file_path):
        """_summary_

        Args:
            file_path (_type_): _description_
        """
        self.save_frame()
        self.image_pointer = len(self.images) - 1
        self.file_name_dict[self.image_pointer] = Path(file_path).name
        self.write_frame()
                
    def set_image(self):
        """Update the displayed images, resizing to fit the label size, keeping aspect ratio, and centering."""
        pil_img = None
        pil_pred_img = None
        if self._original_images and self.image_pointer < len(self._original_images):
            pil_img = self._original_images[self.image_pointer]
        if self._original_pred_images and self.image_pointer < len(self._original_pred_images):
            pil_pred_img = self._original_pred_images[self.image_pointer]
        lw = self.images_frame.left_window
        rw = self.images_frame.right_window
        
        lw_w = lw.winfo_width()
        lw_w = lw_w if lw_w not in (None, 0, 1) else THUMBNAIL_SIZE[0]
        lw_h = lw.winfo_height()
        lw_h = lw_h if lw_h not in (None, 0, 1) else THUMBNAIL_SIZE[1]
        rw_w = rw.winfo_width()
        rw_w = rw_w if rw_w not in (None, 0, 1) else THUMBNAIL_SIZE[0]
        rw_h = rw.winfo_height()
        rw_h = rw_h if rw_h not in (None, 0, 1) else THUMBNAIL_SIZE[1]
                
        def resize_and_center(pil_img, box_w, box_h):
            if pil_img is None:
                return self.black_photoimage
            img_w, img_h = pil_img.size
            scale = min(box_w / img_w, box_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            img_resized = pil_img.copy().resize((new_w, new_h), Image.LANCZOS)
            # Create black background
            bg = Image.new('RGB', (box_w, box_h), (0, 0, 0))
            # Center the image
            x = (box_w - new_w) // 2
            y = (box_h - new_h) // 2
            bg.paste(img_resized, (x, y))
            return PhotoImage(bg)
        # Left image
        lw_img = resize_and_center(pil_img, lw_w, lw_h)
        lw.image = lw_img
        lw.config(image=lw_img)
        # Right image
        rw_img = resize_and_center(pil_pred_img, rw_w, rw_h)
        rw.image = rw_img
        rw.config(image=rw_img)
        if len(self.images) == 0:
            self.images_frame.counter.config(text='-/0')
        else:
            self.images_frame.counter.config(text=f'{self.image_pointer + 1}/{len(self.images)}')
    
    def set_prediction_image(self, prediction_image_pointer, file_path):
        if len(self.images) == 0:
            return
        assert prediction_image_pointer >= 0 and prediction_image_pointer <= len(self.images) - 1
        self.image_pointer = prediction_image_pointer
        # Store original PIL prediction image
        if file_path == None:
            pil_pred_img = None
        else:
            pil_pred_img = Image.open(file_path)
            
        if len(self._original_pred_images) <= prediction_image_pointer:
            self._original_pred_images.extend([None] * (prediction_image_pointer + 1 - len(self._original_pred_images)))
        try:
            self._original_pred_images[prediction_image_pointer] = pil_pred_img.copy()
        except AttributeError:
            self._original_pred_images[prediction_image_pointer] = None
        self.prediction_images[prediction_image_pointer] = file_path
        self.set_image()
    
    def clear_all_images(self):
        self.image_pointer = 0
        self.images_frame.right_window.config(image=self.black_photoimage)
        self.images_frame.left_window.config(image=self.black_photoimage)
        self.images = ImageList(name=f'True{self.name}')
        self.top_frame_saves = {}
        self.output_frame_saves = {}
        self.prediction_images = ImageList(name=f'Pred{self.name}')
        self._original_images = []
        self._original_pred_images = []
        widgets = self.top_frame_widgets
        for key in self.top_frame_widgets:
            widgets[key].push(None)
        widgets = self.output_frame_widgets
        for key in self.output_frame_widgets:
            widgets[key].push(None)
        self.images_frame.counter.config(text='-/0')

    def _on_images_frame_resize(self, event):
        """Handle resizing of the images_frame to update image sizes."""
        self.set_image()

    def take_image(self):
        """Open a window with a live camera feed and capture/cancel buttons."""
        # Disable the button while camera window is open
        self.images_frame.take_image.config(state='disabled')
        self._open_camera_window()

    def _open_camera_window(self):
        import threading
        import tkinter.messagebox as mb
        from PIL import Image, ImageTk
        import tkinter as tk
        # Camera setup
        use_picamera2 = False
        if is_raspberry_pi() and has_picamera2():
            use_picamera2 = True
        if use_picamera2:
            try:
                from picamera2 import Picamera2 # type: ignore
                import numpy as np
            except ImportError:
                mb.showerror('Camera Error', 'picamera2 is not installed')
                self.images_frame.take_image.config(state='normal')  # Re-enable button on error
                return
            picam = Picamera2()
            config = picam.create_preview_configuration()
            picam.configure(config)
            picam.start()
            # Get camera resolution
            cam_res = picam.capture_metadata()['ScalerCrop'][2:]
            native_width, native_height = cam_res if cam_res else (640, 480)
        else:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                mb.showerror('Camera Error', 'Could not open webcam')
                self.images_frame.take_image.config(state='normal')  # Re-enable button on error
                return
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 9999)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 9999)
            native_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            native_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect = native_width / native_height if native_height != 0 else 4/3
        # Get screen size and set initial window size
        root = self.winfo_toplevel()
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        max_preview_w = int(screen_w * 0.8)
        max_preview_h = int(screen_h * 0.7)
        if max_preview_w / aspect <= max_preview_h:
            preview_w = max_preview_w
            preview_h = int(max_preview_w / aspect)
        else:
            preview_h = max_preview_h
            preview_w = int(max_preview_h * aspect)
        button_area = 60
        extra_margin = 30
        total_height = preview_h + button_area + extra_margin
        # Create a new Toplevel window
        cam_win = tk.Toplevel(self)
        cam_win.title('Camera')
        cam_win.geometry(f'{preview_w}x{total_height}')
        cam_win.minsize(320, 240 + button_area + extra_margin)
        cam_win.resizable(True, True)
        # Camera frame
        video_frame = ttk.Label(cam_win)
        video_frame.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)
        # Buttons
        btn_frame = ttk.Frame(cam_win)
        btn_frame.pack(pady=(10, 20))
        capture_btn = ttk.Button(btn_frame, text='Capture')
        cancel_btn = ttk.Button(btn_frame, text='Cancel')
        capture_btn.grid(row=0, column=0, padx=20)
        cancel_btn.grid(row=0, column=1, padx=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        # State
        self._camera_running = True
        self._camera_frame = None
        self._last_preview_size = (preview_w, preview_h)
        def update_frame():
            if not self._camera_running:
                return
            if use_picamera2:
                frame = picam.capture_array()
                self._camera_frame = frame.copy()
                w, h = self._last_preview_size
                preview_img = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                preview_pil = Image.fromarray(preview_img)
                preview_pil = preview_pil.resize((w, h))
                imgtk = ImageTk.PhotoImage(image=preview_pil)
                video_frame.imgtk = imgtk
                video_frame.config(image=imgtk)
            else:
                ret, frame = cap.read()
                if ret:
                    self._camera_frame = frame.copy()
                    w, h = self._last_preview_size
                    preview_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    preview_pil = Image.fromarray(preview_img)
                    preview_pil = preview_pil.resize((w, h))
                    imgtk = ImageTk.PhotoImage(image=preview_pil)
                    video_frame.imgtk = imgtk
                    video_frame.config(image=imgtk)
            cam_win.after(20, update_frame)
        def on_resize(event):
            win_w = cam_win.winfo_width() - 20
            win_h = cam_win.winfo_height() - button_area - extra_margin - 20
            if win_w / aspect <= win_h:
                new_w = max(1, win_w)
                new_h = max(1, int(win_w / aspect))
            else:
                new_h = max(1, win_h)
                new_w = max(1, int(win_h * aspect))
            self._last_preview_size = (new_w, new_h)
        cam_win.bind('<Configure>', on_resize)
        def on_capture():
            if self._camera_frame is not None:
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                    img_path = tmp.name
                    # Convert color before saving captured frame
                    frame = self._camera_frame.copy()
                    if use_picamera2:
                        # Convert RGBA camera frame to BGR for correct color saving
                        frame_to_save = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                    else:
                        # Frame is already in BGR format
                        frame_to_save = frame
                    cv2.imwrite(img_path, frame_to_save)
                pil_img = Image.open(img_path)
                self._original_images.append(pil_img.copy())
                self.images.append(img_path)
                self.prediction_images.append(None)
                self._original_pred_images.append(None)
                self.update_image(img_path)
                self.set_image() 
            cleanup()
        def on_cancel():
            cleanup()
        def cleanup():
            if use_picamera2:
                picam.stop()
                picam.close()
            else:
                cap.release()
            self._camera_running = False
            self.images_frame.take_image.config(state='normal')  # Re-enable the button
            cam_win.destroy()
        capture_btn.config(command=on_capture)
        cancel_btn.config(command=on_cancel)
        cam_win.protocol('WM_DELETE_WINDOW', on_cancel)
        update_frame()

    def show_fullscreen_image(self, which):
        """Display the selected image (left or right) in a fullscreen Toplevel window."""
        import tkinter as tk
        from PIL import ImageTk
        # Get the image to display
        if which == 'left':
            pil_img = None
            if self._original_images and self.image_pointer < len(self._original_images):
                pil_img = self._original_images[self.image_pointer]
        elif which == 'right':
            pil_img = None
            if self._original_pred_images and self.image_pointer < len(self._original_pred_images):
                pil_img = self._original_pred_images[self.image_pointer]
        else:
            return
        if pil_img is None:
            return
        # Create fullscreen window
        win = tk.Toplevel(self)
        win.title('Fullscreen Image')
        win.attributes('-fullscreen', True)
        win.configure(bg='black')
        # Close on click or Escape
        win.bind('<Escape>', lambda e: win.destroy())
        win.bind('<Button-1>', lambda e: win.destroy())
        # Get screen size
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        # Resize image to fit screen, maintaining aspect ratio
        img_w, img_h = pil_img.size
        scale = min(screen_w / img_w, screen_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        img_resized = pil_img.copy().resize((new_w, new_h), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(img_resized)
        label = tk.Label(win, image=imgtk, bg='black')
        label.image = imgtk  # Keep reference
        label.pack(expand=True)
        # Add a close button in the top-right corner
        close_btn = tk.Label(
            win,
            text='X',
            bg='white',
            fg='black',
            font=('Arial', 24, 'bold'),
            width=2,
            height=1
        )
        close_btn.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
        close_btn.bind('<Button-1>', lambda e: win.destroy())

def get_model_path(relative_path):
    """Helper function to get model path with environment variable support"""
    model_path = Path(relative_path)
    if os.environ.get('DEVISION_MODELS'):
        # If we're in a bundled app, use the environment variable path
        if str(model_path).startswith('models'):
            subdir = ""
            if 'models/' in str(model_path):
                subdir = str(model_path).split('models/', 1)[1]
            model_path = Path(os.environ.get('DEVISION_MODELS')) / subdir
            print(f"Using bundled model path: {model_path}")
    return model_path

def get_annotation_path(relative_path):
    """Helper function to get annotation path with environment variable support"""
    annotation_path = Path(relative_path)
    if os.environ.get('DEVISION_ANNOTATIONS'):
        # If we're in a bundled app, use the environment variable path
        if str(annotation_path).startswith('annotations'):
            subdir = ""
            if 'annotations/' in str(annotation_path):
                subdir = str(annotation_path).split('annotations/', 1)[1]
            annotation_path = Path(os.environ.get('DEVISION_ANNOTATIONS')) / subdir
            print(f"Using bundled annotation path: {annotation_path}")
    return annotation_path

def get_images_path(relative_path):
    """Helper function to get images path with environment variable support"""
    images_path = Path(relative_path)
    if os.environ.get('DEVISION_IMAGES'):
        # If we're in a bundled app, use the environment variable path
        if str(images_path).startswith('images'):
            subdir = ""
            if 'images/' in str(images_path):
                subdir = str(images_path).split('images/', 1)[1]
            images_path = Path(os.environ.get('DEVISION_IMAGES')) / subdir
            print(f"Using bundled images path: {images_path}")
    return images_path

def get_excel_path(relative_path):
    """Helper function to get excel path with environment variable support"""
    excel_path = Path(relative_path)
    if os.environ.get('DEVISION_EXCEL'):
        # If we're in a bundled app, use the environment variable path
        if str(excel_path).startswith('excel'):
            subdir = ""
            if 'excel/' in str(excel_path):
                subdir = str(excel_path).split('excel/', 1)[1]
            excel_path = Path(os.environ.get('DEVISION_EXCEL')) / subdir
            print(f"Using bundled excel path: {excel_path}")
    return excel_path

def get_output_dir(name):
    """Return a persistent output directory, next to the EXE when frozen, else cwd."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.getcwd()
    out_dir = os.path.join(base, name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

class OysterPage(Page):
    def __init__(self, *args, **kwargs):
        self.name = "Oyster"
        super().__init__(*args, **kwargs)
        # Ensure csv_path exists in user settings
        if 'csv_path' not in SettingsWindow._settings:
            SettingsWindow._settings['csv_path'] = ''
        
        self.help_window_open = False
        self.brood_count_dict = {}
        self.excel_obj = OysterExcel()
        self.settings_obj = SettingsWindow()
        self.settings = self.settings_obj.settings
        
        self.model_select = self.add_input(DropdownBox, text="Model Select", dropdowns=[
            "2-4mm model",
            "4-6mm model",
            "Select a Model from Folder"
        ])
        # Give the Model Select column a higher weight and minsize to prevent shrinking
        self.top_frame.columnconfigure(0, weight=3, minsize=180)
        
        self.add_input(LabelBox, text='Group Number')
        self.add_input(LabelBox, text='Size Class')
        self.add_input(LabelBox, text='Seed Tray Weight (g)')
        self.add_input(LabelBox, text='Slide Weight (g)')
        self.add_input(LabelBox, text='Slide + Seed Weight (g)')
       
        # Add the settings buttons in a single row
        self.predict_button = self.add_settings(IOButton, text='Predict Brood Count', command=self.get_prediction, disable_during_run=True)
        self.add_settings(IOButton, text='Append to CSV File', command=self.load_csv)
        self.add_settings(IOButton, text='Predict all and Export', command=self.to_csv, disable_during_run=True)
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        self.add_settings(IOButton, text='Help', command=self.open_help)
        
        self.predict_counter = self.add_output(Counter, text='Oyster Brood Count')
        self.model_error_label = self.add_output(ErrorLabel, text='')
        self.progress_bar = self.add_output(ProgressBar)
        self.progress = 100
        
        self.predict_button.bind_out(self.predict_counter)
        
        # Bind callback to model_select dropdown to clear error label when a valid model is selected
        def clear_error_on_select(*args):
            value = self.model_select.value
            if value != 'None' and value:
                self.model_error_label.push(None)
        self.model_select.menu_var.trace_add('write', clear_error_on_select)
        
    def get_prediction(self, img_pointer=None, auto_export=True):
        # Hide error label by default
        self.model_error_label.push(None)
        
        if img_pointer is None:
            img_pointer = self.image_pointer
        
        if len(self.images) == 0  or img_pointer >= len(self.images) or img_pointer < 0:
            return 0
        
        model_path = self.model_select.value
        if model_path is None:
            self.model_error_label.push('Please select a model before predicting.')
            return 0
        classes = 1  # Default value
        if model_path == '2-4mm model':
            model_path = get_model_path('models/oyster_2-4mm')
        elif model_path == '4-6mm model':
            model_path = get_model_path('models/oyster_4-6mm')
        elif model_path == 'choose a model from folder':
            model_path = get_model_path(askdirectory(title='Please select a model directory'))
        else:
            self.model_error_label.push('Please select a model before predicting.')
            return 0
        
        # Always use img_pointer for image and annotation
        with Image.open(self.images.paths[img_pointer]) as img:  
            annotate = self.settings['toggles']['annotate-default']
            api = ModelAPI(model_path, img, classes, annotate)   
            count, annotation = api.get()

        # Determine where to save annotations
        if annotation:
            anno_dir = self.settings['annotation_path']
            if self.settings['toggles']['autosave-image-default']:
                # Prompt user for annotation directory on first use
                if not anno_dir:
                    selected = askdirectory(
                        initialdir=get_annotation_path('annotations'),
                        title='Select folder to save annotation images'
                    )
                    if selected:
                        anno_dir = selected
                        # Persist choice
                        SettingsWindow._settings['annotation_path'] = anno_dir
                        self.settings_obj.write_user_settings()
                # Build full annotation file path
                if anno_dir:
                    annotation_fp = os.path.join(anno_dir, f"oysterannotation{img_pointer}.png")
                else:
                    # Fallback to persistent annotations folder
                    fallback_dir = get_output_dir('annotations')
                    annotation_fp = os.path.join(fallback_dir, f"oysterannotation{img_pointer}.png")
                # Save the annotation image
                try:
                    os.makedirs(os.path.dirname(annotation_fp), exist_ok=True)
                    annotation.save(fp=annotation_fp)
                except Exception as e:
                    print(f"Warning: Could not save annotation: {str(e)}")
        else:
            annotation_fp = None
        self.brood_count_dict[img_pointer] = count
        self.set_prediction_image(img_pointer, annotation_fp)
        
        # Auto-export to CSV only if enabled and this call allows it
        if auto_export and self.settings['toggles']['excel-default']:
            self.to_csv(predict_all=False)
        
        if self.settings['toggles']['clear-excel-default']:
            self.excel_obj = OysterExcel()
            
        return count
    
    def open_help(self):
        def on_destroy(event):
            self.help_window_open = False
        
        if not self.help_window_open:
            help_markdown_path = Path('data/oyster-help.md')
            with open(help_markdown_path) as file:
                raw_str = file.read()
            
            help_window = Markdown(self, raw_str)
            help_window.bind('<Destroy>', on_destroy)
            
            self.help_window_open = True
    
    def write_frame(self):
        super().write_frame()
        if hasattr(self, 'progress_bar'):
            self.progress_bar.push(self.progress)
    
    def to_csv(self, drop_na=True, predict_all=True):
        # Determine export directory from user settings
        export_dir = SettingsWindow._settings.get('csv_path', '')
        # Full export: ask for folder if not already set
        if predict_all:
            if not export_dir:
                dir_selected = askdirectory(
                    initialdir=get_excel_path('excel'),
                    title='Select folder to save CSV files'
                )
                if not dir_selected:
                    return
                export_dir = dir_selected
                SettingsWindow._settings['csv_path'] = export_dir
                self.settings_obj.write_user_settings()
            # Reset data and predict all without individual exports
            self.excel_obj = OysterExcel()
            
            self.disable_move_buttons()
            self.predict_button.button.config(state='disabled')
            for img_pointer in range(len(self.images)):
                self.save_frame()
                self.img_pointer = img_pointer
                self.write_frame()
                self.progress = 100 * img_pointer / len(self.images)
                self.progress_bar.push(self.progress)
                if img_pointer not in self.brood_count_dict:
                    count = self.get_prediction(img_pointer, auto_export=False)
                    self.predict_counter.push(count)
            self.progress = 100
            self.progress_bar.push(self.progress)
            self.enable_move_buttons()
            self.predict_button.button.config(state='normal')
            
        data = self.get_all_inputs()

        df = pd.DataFrame.from_dict(data, orient='index')
        df_file = pd.DataFrame.from_dict(self.file_name_dict, orient='index')
        df_count = pd.DataFrame.from_dict(self.brood_count_dict, orient='index')
     
        df = pd.concat(objs=[df, df_file, df_count], axis=1, ignore_index = True)
        
        if drop_na:
            df = df.dropna(how='any')
            df = df[~df.isin(['']).any(axis=1)]
        
        if df.empty:
            return
        
        df = df.rename(columns={0:'model', 1:'group', 2:'size-class', 3:'seed-tray-weight', 4:'slide-weight', 5:'slide-and-seed-weight', 6:'file-name', 7:'subsample-count'})
        
        numeric_columns = ['seed-tray-weight', 'slide-weight', 'slide-and-seed-weight', 'subsample-count']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])

        # Append only the last record when doing incremental export
        if predict_all:
            df_to_export = df
        else:
            df_to_export = df.tail(1)

        # Fallback to persistent csv folder when no user setting is provided
        if not export_dir:
            export_dir = get_output_dir('excel')
        base_path = os.path.join(export_dir, f'data{self.excel_obj.id}')
        self.excel_obj.extend(df_to_export)
        self.excel_obj.write_csv(base_path=base_path)
        
    # For backward compatibility
    def to_excel(self, drop_na=True, predict_all=True):
        return self.to_csv(drop_na, predict_all)
    
    def load_csv(self):        
        initialdir = get_excel_path('excel')
        # Always ensure the directory exists
        try:
            os.makedirs(initialdir, exist_ok=True)
            print(f"Ensured excel directory exists: {initialdir}")
        except Exception as e:
            print(f"Warning: Could not create excel directory: {str(e)}")
        
        file_path = askopenfilename(
            initialdir=initialdir,
            title='Please select a CSV file to open',
            filetypes=[('CSV Files', '*.csv'), ('Excel Files', '*.xlsx *.xlsb *.xltx *.xltm *.xls *.xlt *.ods')]
        )
        
        if file_path == ():
            return
        
        if Path(file_path).suffix not in ['.csv', '.xlsx', '.xlsb', '.xltx', '.xltm', '.xls', '.xlt', '.ods']:
            return

        self.excel_obj.read_csv(file_path)
    
    def clear_all_images(self):
        super().clear_all_images()
        if self.settings['toggles']['clear-output-default']:
            self.excel_obj = OysterExcel()
        
    def open_settings(self):
        Settings(self)
    
#TODO: Add group number
#TODO: Add temperature
class DevisionPage(Page):
    def __init__(self, *args, **kwargs):
        self.name = "Devision"
        super().__init__(*args, **kwargs)
        
        self.help_window_open = False
        self.egg_count_dict = {}
        self.class_count_dicts = {}
        self.settings_obj = SettingsWindow()
        self.settings = self.settings_obj.settings
        self.model_names = ['Frog Egg Counter', 
                            'Xenopus 4 Class Counter',
                            'Select a Model from Folder'
                           ]
        self.progress = 100
        
        #This button resizes at runtime and there's no built in way to change a ttk widget's width
        self.model_select = self.add_input(DropdownBox, text='Select a Model Below', dropdowns=self.model_names)
        
        self.predict_button: IOButton = self.add_settings(IOButton, text='Predict and Annotate', command=self.get_prediction, disable_during_run=True)
        self.add_settings(IOButton, text='Export to CSV', command=self.to_csv)
        self.add_settings(IOButton, text='Predict All', command=self.predict_all, disable_during_run=True)
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        self.add_settings(IOButton, text='Help', command=self.open_help)

        
        self.predict_counter = self.add_output(Counter, text='Model Count')
        self.model_error_label = self.add_output(ErrorLabel, text='')
        self.progress_bar = self.add_output(ProgressBar)

       
        self.predict_button.bind_out(self.predict_counter)
    
    def write_frame(self):
        out =  super().write_frame()
        if hasattr(self, 'progress_bar'):
            self.progress_bar.push(self.progress)
        return out
    
    def predict_all(self):
        self.disable_move_buttons()
        self.predict_button.button.config(state='disabled')
        for img_pointer in range(len(self.images)):
            self.save_frame()
            self.img_pointer = img_pointer
            self.write_frame()
            self.progress = 100 * img_pointer / len(self.images)
            self.progress_bar.push(self.progress)
            if img_pointer not in self.egg_count_dict:
                count = self.get_prediction(img_pointer)
                self.predict_counter.push(count)
        self.progress = 100
        self.progress_bar.push(self.progress)
        self.enable_move_buttons()
        self.predict_button.button.config(state='normal')
    
    def get_prediction(self, img_pointer=None):
        self.model_error_label.push(None)
        
        if not img_pointer:
            img_pointer = self.image_pointer
        
        if len(self.images) == 0  or img_pointer >= len(self.images) or img_pointer < 0:
            return 0
                
        model_str = self.model_select.value
        if model_str == self.model_names[1]:
            model_dir = get_model_path('models/xenopus-4-class-v2')
            classes = 4
        elif model_str == self.model_names[0]:
            model_dir = get_model_path('models/frog-egg-counter')
            classes = 1
        elif model_str == self.model_names[2]:
            model_dir = get_model_path(askdirectory(title='Please select a model directory'))
            classes = 1

        else:
            self.model_error_label.push('Failed to load model: Please select a valid model.')
            return 0
        
        with Image.open(self.images.paths[img_pointer]) as img:
            annotate = self.settings['toggles']['annotate-default']
            api = ModelAPI(model_dir, img, classes, annotate)
            count, annotation = api.get()
        
        if annotation:
            annotation_fp = get_annotation_path(f"annotations/devisionannotation{self.image_pointer}.png")
            if self.settings['toggles']['autosave-image-default']:
                # Ensure annotations directory exists
                try:
                    os.makedirs(os.path.dirname(annotation_fp), exist_ok=True)
                    annotation.save(fp=annotation_fp)
                except Exception as e:
                    print(f"Warning: Could not save annotation: {str(e)}")
        else:
            annotation_fp = None
        self.class_count_dicts[img_pointer] = api.count_dct.copy()
        self.egg_count_dict[img_pointer] = count
        self.set_prediction_image(img_pointer, annotation_fp)
        return count
    
    def open_settings(self):
        Settings(self)
    
    def open_help(self):
        def on_destroy(event):
            self.help_window_open = False
        
        if not self.help_window_open:
            help_markdown_path = Path('data/devision-help.md')
            with open(help_markdown_path) as file:
                raw_str = file.read()
            
            help_window = Markdown(self, raw_str)
            help_window.bind('<Destroy>', on_destroy)
            
            self.help_window_open = True
            
    def to_csv(self):
        date = datetime.datetime.now()
        files: dict = self.file_name_dict
        counts: dict = self.egg_count_dict
        models: dict = self.get_all_inputs()[0]
        count_dicts: dict = self.class_count_dicts
        
        data = [{'Datetime':date, 'Model':model, 'Filename':file, 'Total Count':count, 
                 'Class 0 Count':count_dct.get(0, 0), 'Class 1 Count': count_dct.get(1, 0), 'Class 2 Count': count_dct.get(2, 0), 'Class 3 Count': count_dct.get(3, 0)} for 
                file, count, model, count_dct in zip(files.values(), counts.values(), models.values(), count_dicts.values())]
        
        df = pd.DataFrame(data, columns=['Datetime', 'Model', 'Filename', 'Total Count',
                                         'Class 0 Count', 'Class 1 Count', 'Class 2 Count', 'Class 3 Count'])
        
        
        df = df.dropna(how='any')
        
        head = SettingsWindow._settings.get('csv_path', './excel')
        if head == '':
            head = './excel'
        export_dir = Path(head) / 'data-devision.csv'
        df.to_csv(export_dir, index=False)
                    
                
if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    
    frog = DevisionPage()
    oyster = OysterPage()
    
    notebook.add(frog, text='Devision Page')
    notebook.add(oyster, text='Oyster Page')
    
    notebook.grid(row=0, column=0, sticky='NSEW')
    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
