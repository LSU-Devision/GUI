# Motivation for this file:
# Being able to create new image-based pages as easy as building blocks as opposed to hand-coding every single widget
# Pages is specifically for image prediction pages like MainFrame and OysterPage, but the concept is
# able to be generalized

from stardist.models import StarDist2D
import numpy as np
from csbdeep.utils import normalize

import tkinter as tk
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory
import json

from tkinter import ttk

from Widgets import *
from SettingsWindow import SettingsWindow, Settings
from OysterExcel import OysterData
from ImageProcessing import ImageList, THUMBNAIL_SIZE, highlight_boundary

from PIL.ImageTk import PhotoImage, getimage
from PIL import Image

import os
from pathlib import Path
import subprocess
import threading
import time
import glob
from queue import Queue, Empty
import tkinter.messagebox as messagebox

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
# There doesn't really exist a way to both resize a tkinter dialog and maintain a dynamically sized image
# This is a motivating example for a website

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
            output_frame_kwargs={'sticky':'NSWE', 'padx':10}
        
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
        if os.path.exists(f'config/ImageListTrue{self.name}.json'):
            with open(f'config/ImageListTrue{self.name}.json', 'r') as file:
                true_json = list(json.load(file))
        if os.path.exists(f'config/ImageListPred{self.name}.json'):
            with open(f'config/ImageListPred{self.name}.json', 'r') as file:
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
        self.images_frame.button_frame.columnconfigure(2, weight=1)
        # Create buttons with same width
        button_width = 20
        self.images_frame.file_select = ttk.Button(self.images_frame.button_frame, text='Select an image', command=self.add_image, style='Image.TButton', width=button_width)
        self.images_frame.take_image = ttk.Button(self.images_frame.button_frame, text='Take an image', command=self.take_image, style='Image.TButton', width=button_width)
        self.images_frame.receive_bt_image = ttk.Button(self.images_frame.button_frame, text='Receive via Bluetooth', command=self.receive_image_bluetooth, style='Image.TButton', width=button_width)
        
        self.images_frame.file_select.grid(row=0, column=0, padx=5, pady=0, sticky='EW')
        self.images_frame.take_image.grid(row=0, column=1, padx=5, pady=0, sticky='EW')
        self.images_frame.receive_bt_image.grid(row=0, column=2, padx=5, pady=0, sticky='EW')
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
        # Remove old button placements (file_select, take_image)
        # self.images_frame.file_select.grid(row=0, column=1, sticky='EW', **self.images_frame_kwargs)
        # self.images_frame.take_image.grid(row=0, column=2, sticky='EW', **self.images_frame_kwargs)
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
            self.update_image(file_path)
            self.set_image()
        
        self.bt_server_process = None
        self.bt_monitor_thread = None
        self.bt_transfer_path = get_bluetooth_transfer_path()
        os.makedirs(self.bt_transfer_path, exist_ok=True)
        self.bt_received_file_queue = Queue()
        self.after(100, self._check_bt_queue)
        
    def _check_bt_queue(self):
        new_file_path = None
        try:
            new_file_path = self.bt_received_file_queue.get_nowait()

            print(f"Processing image from BT queue: {new_file_path}")
            try:
                pil_img = Image.open(new_file_path)
                self._original_images.append(pil_img.copy())
                pil_img.close()

                self.images.append(new_file_path)
                self.prediction_images.append(None)
                self._original_pred_images.append(None)

                self.update_image(new_file_path) # Sets image_pointer correctly
                self.set_image() # Displays the new image

                messagebox.showinfo("Bluetooth Transfer", f"Successfully received and loaded: {os.path.basename(new_file_path)}")
                
            except FileNotFoundError:
                print(f"Error: File {new_file_path} not found during BT processing.")
                if new_file_path: # Avoid error if new_file_path itself is None (shouldn't happen here)
                    messagebox.showerror("File Error", f"Failed to load: {os.path.basename(new_file_path)}\nFile not found.")
            except Image.UnidentifiedImageError:
                print(f"Error: Could not open or read image file {new_file_path} (unidentified image).")
                if new_file_path:
                    messagebox.showerror("Image Error", f"Failed to load: {os.path.basename(new_file_path)}\nNot a valid image file or format.")
            except Exception as img_proc_e: # Catch other image processing errors
                print(f"Error processing image {new_file_path} from BT: {img_proc_e}")
                if new_file_path:
                    messagebox.showerror("Processing Error", f"Error processing image: {os.path.basename(new_file_path)}\nDetails: {img_proc_e}")

        except Empty: # Handles empty queue
            pass # No new file in the queue, do nothing this cycle
        except Exception as e:
            # Catch other unexpected errors in the _check_bt_queue logic itself
            print(f"Unexpected error in _check_bt_queue (outside image processing): {e}")
        finally:
            # Always reschedule the check
            self.after(100, self._check_bt_queue)

    def _get_ip_address(self):
        try:
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, check=True)
            return result.stdout.strip().split(' ')[0]
        except Exception as e:
            print(f"Could not determine IP address using 'hostname -I': {e}")
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except Exception as e_sock:
                print(f"Socket method to get IP also failed: {e_sock}")
                return None

    def receive_image_bluetooth(self):
        if self.bt_server_process and self.bt_server_process.poll() is None:
            messagebox.showwarning("Bluetooth Server", "Server is already running. Check terminal for IP or upload from phone.")
            return

        ip_address = self._get_ip_address()
        if not ip_address:
            messagebox.showerror("Network Error", "Could not determine the IP address of this device. Cannot start Bluetooth server.")
            self.images_frame.receive_bt_image.config(state='normal') # Re-enable button
            return

        script_path = os.path.join(Path(__file__).resolve().parent.parent, "bt_file_server.py") 

        if not os.path.exists(script_path):
            messagebox.showerror("File Error", f"Server script not found at {script_path}")
            self.images_frame.receive_bt_image.config(state='normal') # Re-enable button
            return
        
        try:
            # Disable the button before starting the server
            self.images_frame.receive_bt_image.config(state='disabled')
            self.bt_server_process = subprocess.Popen([sys.executable, script_path])
            print(f"Bluetooth server script started (PID: {self.bt_server_process.pid}). Check its console output for status.")
        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to start Bluetooth server: {e}")
            self.bt_server_process = None
            self.images_frame.receive_bt_image.config(state='normal') # Re-enable button on failure
            return

        instructions = (
            f"Bluetooth photo server started.\n\n"
            f"1. Ensure your phone is PAIRED with this Raspberry Pi via Bluetooth.\n"
            f"2. Ensure Bluetooth PAN (Personal Area Network) is active on the Pi.\n"
            f"   (The system service 'bt-pan.service' should be running).\n"
            f"3. On your phone, open a web browser and go to:\n"
            f"   http://{ip_address}:4020\n\n"
            f"4. Upload your photo using the web page.\n"
            f"The photo will appear here automatically after upload."
        )
        messagebox.showinfo("Receive via Bluetooth", instructions)

        if self.bt_monitor_thread is None or not self.bt_monitor_thread.is_alive():
            self.bt_monitor_thread = threading.Thread(target=self._monitor_bluetooth_transfers, daemon=True)
            self.bt_monitor_thread.start()

    def _monitor_bluetooth_transfers(self):
        print(f"Monitoring {self.bt_transfer_path} for new files...")
        seen_files = set(os.listdir(self.bt_transfer_path))

        while True:
            if self.bt_server_process is None or self.bt_server_process.poll() is not None:
                print("Bluetooth server process stopped or not found. Stopping monitor.")
                break
            
            try:
                current_files_basenames = set(os.listdir(self.bt_transfer_path))
                newly_added_basenames = current_files_basenames - seen_files

                if newly_added_basenames:
                    for basename in newly_added_basenames:
                        full_path = os.path.join(self.bt_transfer_path, basename)
                        if os.path.isfile(full_path): # Ensure it's a file
                            print(f"New file detected: {full_path}")
                            self.bt_received_file_queue.put(full_path)
                            seen_files.add(basename) # Add basename to seen_files

            except FileNotFoundError:
                print(f"Monitoring path {self.bt_transfer_path} not found. Stopping monitor.")
                break # Stop monitoring if the path itself disappears
            except Exception as e:
                print(f"Error in Bluetooth monitoring thread: {e}")
                # Add a small delay to prevent rapid error logging if persistent issue
                time.sleep(1)
            
            time.sleep(1) # Poll every second
        print("Bluetooth monitoring thread finished.")

    def _stop_bt_server_and_monitor(self):
        if self.bt_server_process and self.bt_server_process.poll() is None:
            print("Stopping Bluetooth server...")
            self.bt_server_process.terminate()
            try:
                self.bt_server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not terminate, killing.")
                self.bt_server_process.kill()
            self.bt_server_process = None
            print("Bluetooth server stopped.")
            # Re-enable the button when server is stopped
            if hasattr(self, 'images_frame') and hasattr(self.images_frame, 'receive_bt_image'):
                self.images_frame.receive_bt_image.config(state='normal')

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
            filetypes=[('Images', '*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG')]
        )
        if not file_paths:
            return
        last_file_path = None
        for file_path in file_paths:
            if Path(file_path).suffix not in ['.jpg', '.JPG', '.jpeg', '.png', '.PNG']:
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
        lw_w = lw.winfo_width() or THUMBNAIL_SIZE[0]
        lw_h = lw.winfo_height() or THUMBNAIL_SIZE[1]
        rw_w = rw.winfo_width() or THUMBNAIL_SIZE[0]
        rw_h = rw.winfo_height() or THUMBNAIL_SIZE[1]
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
            self.images_frame.counter.config(text='0/0')
        else:
            self.images_frame.counter.config(text=f'{self.image_pointer + 1}/{len(self.images)}')
    
    def set_prediction_image(self, prediction_image_pointer, file_path):
        if len(self.images) == 0:
            return
        assert prediction_image_pointer >= 0 and prediction_image_pointer <= len(self.images) - 1
        self.image_pointer = prediction_image_pointer
        # Store original PIL prediction image
        pil_pred_img = Image.open(file_path)
        if len(self._original_pred_images) <= prediction_image_pointer:
            self._original_pred_images.extend([None] * (prediction_image_pointer + 1 - len(self._original_pred_images)))
        self._original_pred_images[prediction_image_pointer] = pil_pred_img.copy()
        self.prediction_images[prediction_image_pointer] = file_path
        self.set_image()
    
    def clear_all_images(self):
        self._stop_bt_server_and_monitor()
        self.images.clear()
        self.prediction_images.clear()
        self._original_images.clear()
        self._original_pred_images.clear()
        self.image_pointer = 0
        self.set_image()
        self.set_prediction_image(None, None)
        self.update_counter()

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
            
            try:
                picam = Picamera2()
                # Try different configuration approaches for autofocus camera compatibility
                try:
                    # First try: Use still configuration which is more stable with autofocus cameras
                    config = picam.create_still_configuration(main={"size": (1920, 1080)})
                    picam.configure(config)
                    picam.start()
                except Exception as config_error:
                    print(f"Still configuration failed: {config_error}")
                    try:
                        # Second try: Use preview configuration with explicit controls
                        config = picam.create_preview_configuration()
                        # Disable autofocus-related controls that might cause issues
                        config["controls"] = {"AfMode": 0}  # Manual focus mode
                        picam.configure(config)
                        picam.start()
                    except Exception as preview_error:
                        print(f"Preview configuration failed: {preview_error}")
                        # Third try: Basic configuration without any controls
                        config = picam.create_preview_configuration()
                        picam.configure(config)
                        picam.start()
                
                # Get camera resolution
                try:
                    cam_res = picam.capture_metadata()['ScalerCrop'][2:]
                    native_width, native_height = cam_res if cam_res else (640, 480)
                except:
                    # Fallback resolution if metadata fails
                    native_width, native_height = (640, 480)
                    
            except Exception as camera_init_error:
                print(f"PiCamera2 initialization failed: {camera_init_error}")
                mb.showerror('Camera Error', f'Failed to initialize Pi Camera: {camera_init_error}\nTrying to use OpenCV fallback...')
                # Fall back to OpenCV
                use_picamera2 = False
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    mb.showerror('Camera Error', 'Could not open any camera')
                    self.images_frame.take_image.config(state='normal')  # Re-enable button on error
                    return
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 9999)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 9999)
                native_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                native_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
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

    def destroy(self):
        self._stop_bt_server_and_monitor()
        super().destroy()

def get_bluetooth_transfer_path():
    """Determines the path for Bluetooth transfers.
    Checks for DEVISION_TRANSFER_PATH environment variable first.
    Defaults to '~/bluetooth_transfers' if not set.
    """
    env_path = os.environ.get('DEVISION_TRANSFER_PATH')
    if env_path:
        return env_path
    return os.path.expanduser("~/bluetooth_transfers")

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
        
        self.brood_count_dict = {}
        self.excel_obj = OysterData()
        self.settings_obj = SettingsWindow()
        self.settings = self.settings_obj.settings
        
        self.model_select = self.add_input(DropdownBox, text="Model Select", dropdowns=[
            "2-4mm model",
            "4-6mm model",
        ])
        # Give the Model Select column a higher weight and minsize to prevent shrinking
        self.top_frame.columnconfigure(0, weight=3, minsize=180)
        
        self.add_input(LabelBox, text='Group Number')
        self.add_input(LabelBox, text='Size Class')
        self.add_input(LabelBox, text='Seed Tray Weight (g)')
        self.add_input(LabelBox, text='Slide Weight (g)')
        self.add_input(LabelBox, text='Slide + Seed Weight (g)')
        
        # Add error label above Predict Brood Count button
        self.model_error_label = ttk.Label(self.settings_frame, text='', foreground='red', font='TkDefaultFont')
        self.model_error_label.grid(row=0, column=0, columnspan=4, sticky='EW', pady=(0, 2))
        
        # Add the settings buttons in a single row
        predict_button = self.add_settings(IOButton, text='Predict Brood Count', command=self.get_prediction, disable_during_run=True)
        self.add_settings(IOButton, text='Append to CSV File', command=self.load_csv)
        self.add_settings(IOButton, text='Predict all and Export', command=self.to_csv, disable_during_run=True)
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        
        predict_counter = self.add_output(Counter, text='Oyster Brood Count')
        self.model_error_label = ttk.Label(self.output_frame, text='', foreground='red', font='TkDefaultFont')
        self.model_error_label.grid(row=0, column=1, sticky='W', padx=(10, 0))
        predict_button.bind_out(predict_counter)
        
        # Bind callback to model_select dropdown to clear error label when a valid model is selected
        def clear_error_on_select(*args):
            value = self.model_select.value
            if value != 'None' and value:
                self.model_error_label.config(text='')
        self.model_select.menu_var.trace_add('write', clear_error_on_select)
        
    def get_prediction(self, img_pointer=None, auto_export=True):
        # Hide error label by default
        self.model_error_label.config(text='')
        
        if img_pointer is None:
            img_pointer = self.image_pointer
        
        if len(self.images) == 0  or img_pointer >= len(self.images) or img_pointer < 0:
            return 0
        
        model_path = self.model_select.value
        if model_path == 'None' or not model_path:
            self.model_error_label.config(text='Please select a model before predicting.')
            return 0
        classes = 1  # Default value
        if model_path == '2-4mm model':
            model_path = get_model_path('models/oyster_2-4mm')
        elif model_path == '4-6mm model':
            model_path = get_model_path('models/oyster_4-6mm')
        else:
            self.model_error_label.config(text='Please select a model before predicting.')
            return 0
        
        # Always use img_pointer for image and annotation
        with Image.open(self.images.paths[img_pointer]) as img:  
            api = ModelAPI(model_path, img, classes)    
            count, annotation = api.get()

        # Determine where to save annotations
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
        
        self.brood_count_dict[img_pointer] = count
        self.set_prediction_image(img_pointer, annotation_fp)
        
        # Auto-export to CSV only if enabled and this call allows it
        if auto_export and self.settings['toggles']['excel-default']:
            self.to_csv(predict_all=False)
        
        if self.settings['toggles']['clear-excel-default']:
            self.excel_obj = OysterData()
            
        return count
    
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
            self.excel_obj = OysterData()
            for img_pointer in range(len(self.images)):
                if img_pointer not in self.brood_count_dict:
                    self.get_prediction(img_pointer, auto_export=False)
        
        data = self.get_all_inputs()

        df = pd.DataFrame.from_dict(data, orient='index')
        df_file = pd.DataFrame.from_dict(self.file_name_dict, orient='index')
        df_count = pd.DataFrame.from_dict(self.brood_count_dict, orient='index')
     
        df = pd.concat(objs=[df, df_file, df_count], axis=1, ignore_index = True)
        
        if drop_na:
            df = df.dropna(how='any')
        
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
            self.excel_obj = OysterData()
        
    def open_settings(self):
        Settings(self)
        
#TODO: Add group number
#TODO: Add temperature    
class DevisionPage(Page):
    def __init__(self, *args, **kwargs):
        self.name = "Devision"
        super().__init__(*args, **kwargs)
        
        self.egg_count_dict = {}
        self.settings_obj = SettingsWindow()
        self.settings = self.settings_obj.settings
        
        #This button resizes at runtime and there's no built in way to change a ttk widget's width
        self.model_select = self.add_input(DropdownBox, text='Select a Model Below', dropdowns = ['Egg Counter - StarDist2D', 'Four Embryo Classification - StarDist2D'])
        
        # Add error label above Predict and Annotate button
        self.model_error_label = ttk.Label(self.settings_frame, text='', foreground='red', font='TkDefaultFont')
        self.model_error_label.grid(row=0, column=0, columnspan=4, sticky='EW', pady=(0, 2))
        
        predict_button = self.add_settings(IOButton, text='Predict and Annotate', command=self.get_prediction, disable_during_run=True)
        self.add_settings(IOButton, text='Export to Excel')
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        self.add_settings(IOButton, text='Help')
        
        predict_counter = self.add_output(Counter, text='Model Count')
        predict_button.bind_out(predict_counter)
    
    def get_prediction(self, img_pointer=None):
        if not img_pointer:
            img_pointer = self.image_pointer
        
        if len(self.images) == 0  or img_pointer >= len(self.images) or img_pointer < 0:
            return 0
                
        model_str = self.model_select.value
        if model_str == 'Four Embryo Classification - StarDist2D':
            model_dir = get_model_path('models/xenopus-4-class')
            classes = 4
        elif model_str == 'Egg Counter - StarDist2D':
            model_dir = get_model_path('models/frog-egg-counter')
            classes = 1
        else:
            self.model_error_label.config(text='Failed to load model: Please select a valid model.')
            return 0
        
        with Image.open(self.images.paths[img_pointer]) as img:
            api = ModelAPI(model_dir, img, classes)
            count, annotation = api.get()
        
        annotation_fp = get_annotation_path(f"annotations/devisionannotation{self.image_pointer}.png")
        if self.settings['toggles']['autosave-image-default']:
            # Ensure annotations directory exists
            try:
                os.makedirs(os.path.dirname(annotation_fp), exist_ok=True)
                annotation.save(fp=annotation_fp)
            except Exception as e:
                print(f"Warning: Could not save annotation: {str(e)}")
        
        
        self.egg_count_dict[img_pointer] = count
        self.set_prediction_image(img_pointer, annotation_fp)
        return count
    
    def open_settings(self):
        Settings(self)
                
if __name__ == '__main__':
    root = tk.Tk()
    notebook = ttk.Notebook(root)
    
    frog = DevisionPage(notebook)
    oyster = OysterPage(notebook)
    
    notebook.add(frog, text='Devision Page')
    notebook.add(oyster, text='Oyster Page')
    
    notebook.grid(row=0, column=0, sticky='NSEW')
    
    def on_tab_changed(event):
        if frog.bt_server_process and frog.bt_server_process.poll() is None:
            frog.bt_server_process.terminate()
            frog.bt_server_process.wait()
            frog.images_frame.receive_bt_image.config(state='normal')
            print("BT server stopped for DevisionPage")
        if oyster.bt_server_process and oyster.bt_server_process.poll() is None:
            oyster.bt_server_process.terminate()
            oyster.bt_server_process.wait()
            oyster.images_frame.receive_bt_image.config(state='normal')
            print("BT server stopped for OysterPage")
    
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Initialize button state for OysterPage on startup (in case it's the default tab)
    # This assumes OysterPage is created and its widgets are available.
    if hasattr(oyster, 'images_frame') and hasattr(oyster.images_frame, 'receive_bt_image'):
        if oyster.bt_server_process and oyster.bt_server_process.poll() is None:
            oyster.images_frame.receive_bt_image.config(state='disabled')
        else:
            oyster.images_frame.receive_bt_image.config(state='normal')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
