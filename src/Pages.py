# Motivation for this file:
# Being able to create new image-based pages as easy as building blocks as opposed to hand-coding every single widget
# Pages is specifically for image prediction pages like MainFrame and OysterPage, but the concept is
# able to be generalized

from stardist.models import StarDist2D
import numpy as np
from csbdeep.utils import normalize

import tkinter as tk
from tkinter.filedialog import askopenfilename
import json

from tkinter import ttk

from Widgets import *
from SettingsWindowProposal import SettingsWindow, Settings
from OysterExcel import OysterExcel
from ImageProcessing import ImageList, THUMBNAIL_SIZE, highlight_boundary

from PIL.ImageTk import PhotoImage, getimage
from PIL import Image

import os
from pathlib import Path

import pandas as pd

INTIAL_DIR = Path.cwd()
# There doesn't really exist a way to both resize a tkinter dialog and maintain a dynamically sized image
# This is a motivating example for a website

class IdNotFoundError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f'Could not find id {self.value}'

class Page(ttk.Frame):
    id = 0
    black_image = Image.new(mode='RGB', color=(0, 0, 0), size=THUMBNAIL_SIZE)    
    def __init__(self,
                 *args,
                 **kwargs):
        
        if 'top_frame_kwargs' not in kwargs:
            top_frame_kwargs={'padx':5, 'pady':5, 'sticky':'NS'}
        if 'settings_frame_kwargs' not in kwargs:
            settings_frame_kwargs={'sticky':'EW', 'padx':10}
        if 'output_frame_kwargs' not in kwargs:
            output_frame_kwargs={'sticky':'NSWE', 'padx':10}
        
        super().__init__(*args)
        
        self.id = Page.id
        Page.id += 1
        
        if not hasattr(self, 'name'):
            self.name = f"Page{self.id}"
        
        self.black_photoimage = PhotoImage(Page.black_image)

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
        
        for row in [0, 2, 3]:
            self.rowconfigure(row, weight=1)
            
        for row in [1]:
            self.rowconfigure(row, weight=10, minsize=600)
        
        for column in range(0,1):
            self.columnconfigure(column, weight=1)  
        
        self.image_pointer = 0
        
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
        
        self.images_frame = ttk.Frame(self)
        self.images_frame_kwargs = {
            'padx':5,
            'pady':10
        }
        self.images_frame.left_window = ttk.Label(self.images_frame, relief='groove', image=self.black_photoimage)
        self.images_frame.right_window = ttk.Label(self.images_frame, relief='groove', image=self.black_photoimage)
        self.images_frame.next_button = ttk.Button(self.images_frame, text='Next', command=self.next)
        self.images_frame.prev_button = ttk.Button(self.images_frame, text='Prev', command=self.prev)
        self.images_frame.counter = ttk.Label(self.images_frame, text='-/0', relief='groove', anchor='center')
        self.images_frame.file_select = ttk.Button(self.images_frame, text='Select an image', command=self.add_image)
        self.images_frame.clear_images = ttk.Button(self.images_frame, text='Clear all images', command=self.clear_all_images)
        
        self.images_frame.left_window.grid(row=1, column=0, rowspan=2, sticky='NSEW', **self.images_frame_kwargs)
        self.images_frame.right_window.grid(row=1, column=2, rowspan=2, sticky='NSEW', **self.images_frame_kwargs)
        self.images_frame.prev_button.grid(row=3, column=0, sticky='', **self.images_frame_kwargs)
        self.images_frame.next_button.grid(row=3, column=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.counter.grid(row=3, column=1, sticky='EW', **self.images_frame_kwargs)
        self.images_frame.file_select.grid(row=0, column=1, sticky='EW', **self.images_frame_kwargs)
        self.images_frame.clear_images.grid(row=2, column=1, stick='EW', **self.images_frame_kwargs)
        
        for row in [0,3]:
            self.images_frame.rowconfigure(row, weight=1)
        for row in [1, 2]:
            self.images_frame.rowconfigure(row, weight=2)
        
        self.images_frame.columnconfigure(0, weight=1)
        self.images_frame.columnconfigure(2, weight=1)
        
        self.top_frame.grid(row=0, column=0, sticky='NSEW')
        self.images_frame.grid(row=1, column=0, sticky='NSEW')
        self.output_frame.grid(row=2, column=0, sticky='NSEW')
        self.settings_frame.grid(row=3, column=0, sticky='NSEW')
        
        self.settings_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        for index in range(len(self.images)):
            file_path = self.images.paths[index]
            self.update_image(file_path)
        
        
    def add_input(self, widget, **kwargs):
        assert issubclass(widget, Inputable)
        widget = widget(self.top_frame, **kwargs)
        
        iid = self.top_frame_iid
        self.top_frame_iid += 1
        
        self.top_frame_widgets[iid] = widget
        self.top_frame.columnconfigure(iid, weight=1)
        
        widget.grid(row=0, column=iid, **self.top_frame_kwargs)
        return widget

    def query_input(self, iid):
        if iid not in self.top_frame_widgets:
            raise IdNotFoundError(iid)
        
        widget = self.top_frame_widgets[iid]
        return widget.value
    
    def get_frame_inputs(self):
        return {self.image_pointer:{iid:self.top_frame_widgets[iid].value for iid in self.top_frame_widgets}}   
    
    def get_all_inputs(self):
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
        top_widgets = tuple(self.top_frame_widgets.keys())
        top_widget_data = tuple(map(lambda x: self.top_frame_widgets[x].pop(), top_widgets))
        self.top_frame_saves[self.image_pointer] = tuple(zip(top_widgets, top_widget_data))
        
        out_widgets = tuple(self.output_frame_widgets.keys())
        out_widget_data = tuple(map(lambda x: self.output_frame_widgets[x].pop(), out_widgets))
        self.output_frame_saves[self.image_pointer] = tuple(zip(out_widgets, out_widget_data))
        
    def write_frame(self):
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
        assert issubclass(widget, ttk.Widget)
        widget = widget(self.settings_frame, **kwargs)
                
        iid = self.settings_frame_iid
        self.settings_frame_iid += 1
        
        self.settings_frame_widgets[iid] = widget
        self.settings_frame.columnconfigure(iid, weight=1)

        widget.grid(row=0, column=iid, **self.settings_frame_kwargs)
        return widget

    def add_output(self, widget, **kwargs):
        assert issubclass(widget, Outputable)
        widget = widget(self.output_frame, **kwargs)
        
        iid = self.output_frame_iid
        self.output_frame_iid += 1
        
        self.output_frame_widgets[iid] = widget
        self.output_frame.columnconfigure(iid, weight=1)
        
        widget.grid(row=0, column=iid, **self.output_frame_kwargs)
        return widget
    
    def next(self):
        if len(self.images) == 0:
            return None
        
        self.save_frame()
        self.image_pointer = min(len(self.images)-1, self.image_pointer + 1)
        self.write_frame()

        self.set_image()
        
    def prev(self):
        if len(self.images) == 0:
            return None
        
        self.save_frame()
        self.image_pointer = max(0, self.image_pointer - 1)
        self.write_frame()
        
        self.set_image()
    
    
    def add_image(self):
        file_path = askopenfilename(
                                initialdir=INTIAL_DIR,
                                title='Please select an image',
                                filetypes=[('Images', '*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG *.tif *.tiff')]
                            )
        if file_path == () or Path(file_path).suffix not in ['.jpg', '.JPG', '.jpeg', '.png', '.PNG', '.tif', '.tiff']:
            return
                
        self.images.append(file_path)
        self.prediction_images.append(None)
        self.update_image(file_path)
        
    def update_image(self, file_path):
        self.save_frame()
        self.image_pointer = len(self.images) - 1
        self.file_name_dict[self.image_pointer] = Path(file_path).name
        self.write_frame()
        
        self.set_image()        
        
        
    def set_image(self):
        current_image = self.images[self.image_pointer]
        current_prediction_image = self.prediction_images[self.image_pointer]
        
        self.images_frame.left_window.config(image=current_image)
        self.images_frame.counter.config(text=f'{self.image_pointer + 1}/{len(self.images)}')

        self.images_frame.right_window.config(image=current_prediction_image)
    
    def set_prediction_image(self, prediction_image_pointer, file_path):
        if len(self.images) == 0:
            return
        
        assert prediction_image_pointer >= 0 and prediction_image_pointer <= len(self.images) - 1
        self.image_pointer = prediction_image_pointer
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
        
        widgets = self.top_frame_widgets
        for key in self.top_frame_widgets:
            widgets[key].push(None)
        
        widgets = self.output_frame_widgets
        for key in self.output_frame_widgets:
            widgets[key].push(None)
        
        self.images_frame.counter.config(text='-/0')

    
class OysterPage(Page):
    def __init__(self, *args, **kwargs):
        self.name = "Oyster"
        super().__init__(*args, **kwargs)
        
        self.brood_count_dict = {}
        self.excel_obj = OysterExcel()
        self.settings_obj = SettingsWindow()
        self.settings = self.settings_obj.settings
        
        self.add_input(LabelBox, text='Group Number')
        self.add_input(LabelBox, text='Size Class')
        self.add_input(LabelBox, text='Seed Tray Weight (g)')
        self.add_input(LabelBox, text='Slide Weight (g)')
        self.add_input(LabelBox, text='Slide + Seed Weight (g)')
        
        #The way this method works is unfortuante, it results both from Tkinter being a bad language (not being able to reassign master widgets) as well as
        #Python not having static typing
        predict_button = self.add_settings(IOButton, text='Predict Brood Count', command=self.get_prediction)
        self.add_settings(IOButton, text='Load Data from Excel', command=self.load_excel)
        self.add_settings(IOButton, text='Export to Excel', command=self.to_excel)
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        
        predict_counter = self.add_output(Counter, text='Oyster Brood Count')
        predict_button.bind_out(predict_counter)
        
    #TODO: Convert this code to use some sort of image processing manager, more than ImageList
    def get_prediction(self, img_pointer=None):
        if not img_pointer:
            img_pointer = self.image_pointer
        
        if len(self.images) == 0  or img_pointer >= len(self.images) or img_pointer < 0:
            return 0
        
        model = StarDist2D(config=None, name='oyster_2-4mm', basedir='models')

        
        img = Image.open(self.images.paths[img_pointer])
        img_arr = img.convert('L')
        img_arr = np.array(img_arr)
        img_arr = normalize(img_arr, 1, 99.8, axis=(0, 1))
        
        labels, details = model.predict_instances(img_arr, n_tiles=model._guess_n_tiles(img_arr))
        
        annotation_fp = f"test/annotations/oysterannotation{self.image_pointer}.png"
        
        mask_image = Image.new(mode='1', color=0, size=img.size)
        mask_image.putdata(labels.flatten())
        annotation = highlight_boundary(img, mask_image, (255, 0, 0), width=4)
        annotation.save(fp=annotation_fp)
        
        img.close()
        
        count = len(details['points'])
        self.brood_count_dict[img_pointer] = count
        self.set_prediction_image(img_pointer, annotation_fp)
        
        #Legacy settings
        if self.settings['toggles']['excel-default']:
            self.to_excel(predict_all=False)
        
        if self.settings['toggles']['clear-excel-default']:
            self.excel_obj = OysterExcel()
            
        return count
    
    def to_excel(self, drop_na=True, predict_all=True):
        if predict_all:
            for img_pointer in range(len(self.images)):
                if img_pointer not in self.brood_count_dict:
                    self.get_prediction(img_pointer)
        
        data = self.get_all_inputs()

        df = pd.DataFrame.from_dict(data, orient='index')
        df_file = pd.DataFrame.from_dict(self.file_name_dict, orient='index')
        df_count = pd.DataFrame.from_dict(self.brood_count_dict, orient='index')
     
        df = pd.concat(objs=[df, df_file, df_count], axis=1, ignore_index = True)
        
        if drop_na:
            df = df.dropna(how='any')
        
        if df.empty:
            return
        
        df = df.rename(columns={0:'group', 1:'size-class', 2:'seed-tray-weight', 3:'slide-weight', 4:'slide-and-seed-weight', 5:'file-name', 6:'subsample-count'})
        
        numeric_columns = ['seed-tray-weight', 'slide-weight', 'slide-and-seed-weight', 'subsample-count']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])

        self.excel_obj.extend(df)
        
        file_path = self.settings['paths']['output-save']
        if file_path:
            if not os.path.exists(Path(file_path).parent) and self.settings['toggles']['create-dir-default']:
                os.makedirs(Path(file_path).parent)
                self.excel_obj.write_excel(file_path + '/data.xlsx')
                
            elif os.path.exists(Path(file_path).parent):
                self.excel_obj.write_excel(file_path=file_path + '/data.xlsx')
                
            else:
                raise FileNotFoundError('The given output directory does not exist, try creating the directories or enabling create directory by default in settings')
        else:
            raise FileNotFoundError('No output directory selected, consider changing the location in settings')
    
    
    def load_excel(self):
        default_file_path = self.settings['paths']['excel-save']
        if default_file_path and os.path.exists(default_file_path):
            file_path = default_file_path
            
        else:
            file_path = askopenfilename(
                initialdir=INTIAL_DIR,
                title='Please select an excel file to open',
                filetypes=[('Excel Files', '*.xlsx *.xlsb *.xltx *.xltm *.xls *.xlt *.ods')]
            )
            
        if Path(file_path).suffix not in '.xlsx .xlsb .xltx .xltm .xls .xlt .ods'.split(' '):
            return

        self.excel_obj.read_excel(file_path)
    
    def clear_all_images(self):
        super().clear_all_images()
        if self.settings['toggles']['clear-output-default']:
            self.excel_obj = OysterExcel()
        
    def open_settings(self):
        Settings(self)
        
        
class DevisionPage(Page):
    def __init__(self, *args, **kwargs):
        self.name = "Devision"
        super().__init__(*args, **kwargs)
        
        self.egg_count_dict = {}
        self.settings = SettingsWindow()
        
        #This button resizes at runtime and there's no built in way to change a ttk widget's width
        self.add_input(DropdownBox, text='Select a Model Below', dropdowns = ['Frog Counter - StarDist2D', 'Frog Classification - StarDist2D'])
        
        predict_button = self.add_settings(IOButton, text='Predict Egg Count', command=self.get_prediction)
        self.add_settings(IOButton, text='Export to Excel')
        self.add_settings(IOButton, text='Settings', command=self.open_settings)
        self.add_settings(IOButton, text='Help')
        
        predict_counter = self.add_output(Counter, text='Frog Egg Count')
        predict_button.bind_out(predict_counter)
    
    def get_prediction(self):
        if len(self.images) == 0:
            return 0
        
        count, image = (0, None)
        self.egg_count_dict[self.image_pointer] = count
        self.set_prediction_image(self.image_pointer, image)
        return count
    
    def open_settings(self):
        Settings(self)
                
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
