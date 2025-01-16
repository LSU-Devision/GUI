import tkinter as tk
from tkinter.filedialog import askopenfilename

from tkinter import ttk
from WarningWindow import MutImmutable

from PIL.ImageTk import PhotoImage
from PIL import Image
from ttkbootstrap import Style

from pathlib import Path

INTIAL_DIR = Path.cwd()
THUMBNAIL_SIZE = (400, 400)
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
            settings_frame_kwargs={'sticky':'NSEW', 'padx':10}
        if 'output_frame_kwargs' not in kwargs:
            output_frame_kwargs={'sticky':'NSWE', 'padx':10}
        
        super().__init__(*args)
        
        self.id = Page.id
        Page.id += 1
        self.black_photoimage = PhotoImage(Page.black_image)

        
        self.top_frame = ttk.Frame(self)
        self.top_frame_iid = 0
        self.top_frame_widgets = {}
        self.top_frame_kwargs = top_frame_kwargs
        self.top_frame_saves = {}

    
        self.output_frame = ttk.Frame(self)
        self.output_frame_iid = 0
        self.output_frame_widgets = {}
        self.output_frame_kwargs = output_frame_kwargs
        
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
        self.images = []
        self.prediction_images = []
        
        self.images_frame = ttk.Frame(self)
        self.images_frame_kwargs = {
            'padx':5,
            'pady':10
        }
        self.images_frame.left_window = ttk.Label(self.images_frame, relief='groove')
        self.images_frame.right_window = ttk.Label(self.images_frame, relief='groove')
        self.images_frame.next_button = ttk.Button(self.images_frame, text='Next', command=self.next)
        self.images_frame.prev_button = ttk.Button(self.images_frame, text='Prev', command=self.prev)
        self.images_frame.counter = ttk.Label(self.images_frame, text='-/0', relief='groove', anchor='center')
        self.images_frame.file_select = ttk.Button(self.images_frame, text='Select an image', command=self.add_image)
        
        self.images_frame.left_window.grid(row=1, column=0, rowspan=2, sticky='NSEW', **self.images_frame_kwargs)
        self.images_frame.right_window.grid(row=1, column=2, rowspan=2, sticky='NSEW', **self.images_frame_kwargs)
        self.images_frame.prev_button.grid(row=3, column=0, sticky='', **self.images_frame_kwargs)
        self.images_frame.next_button.grid(row=3, column=2, sticky='', **self.images_frame_kwargs)
        self.images_frame.counter.grid(row=3, column=1, sticky='EW', **self.images_frame_kwargs)
        self.images_frame.file_select.grid(row=0, column=1, sticky='EW', **self.images_frame_kwargs)
        
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
        return widget.input
    
    def save_inputs(self):
        widgets = tuple(self.top_frame_widgets.keys())
        widget_data = tuple(map(lambda x: self.top_frame_widgets[x].pop(), widgets))
        self.top_frame_saves[self.image_pointer] = zip(widgets, widget_data)
        
    def write_inputs(self):
        if self.image_pointer not in self.top_frame_saves:
            return
        
        widget_data = self.top_frame_saves[self.image_pointer]
        for widget in widget_data:
            self.top_frame_widgets[widget[0]].push(widget[1])
        
        
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
        if len(self.images) == self.image_pointer + 1:
            return None
        
        self.save_inputs()
        self.image_pointer = min(len(self.images), self.image_pointer + 1)
        self.write_inputs()

        self.set_image()
        
    def prev(self):
        if len(self.images) == 0:
            return None
        
        self.save_inputs()
        self.image_pointer = max(0, self.image_pointer - 1)
        self.write_inputs()
        
        self.set_image()
    
    
    def add_image(self):
        file_path = askopenfilename(
                                initialdir=INTIAL_DIR,
                                title='Please select an image',
                                filetypes=[('Images', '*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG *.tif *.tiff')]
                            )
                                          
        img = Image.open(file_path)
        save_img = img.resize(THUMBNAIL_SIZE)
        save_img = PhotoImage(save_img.convert('RGB'))
        img.close()
        
        self.images.append(save_img)
        self.prediction_images.append(None)
        
        self.save_inputs()
        self.image_pointer = len(self.images) - 1
        self.write_inputs()
        
        self.set_image()        
        
        
    def set_image(self):
        current_image = self.images[self.image_pointer]
        current_prediction_image = self.prediction_images[self.image_pointer]
        
        self.images_frame.left_window.config(image=current_image)
        self.images_frame.counter.config(text=f'{self.image_pointer + 1}/{len(self.images)}')

        if current_prediction_image:
            self.images_frame.right_window.config(image=current_prediction_image)
        else:
            self.images_frame.right_window.config(image=self.black_photoimage)
    
    def set_prediction_image(self, prediction_image_pointer, img):
        if len(self.images) == 0:
            return
        
        assert prediction_image_pointer >= 0 and prediction_image_pointer <= len(self.images) - 1
        self.image_pointer = prediction_image_pointer
        self.prediction_images[prediction_image_pointer] = img
        self.set_image()
    
class TkIO(ttk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self._value = MutImmutable()
    
    #Abstract method
    def pop(self):
        current_input = self._value['']
        self._value = None
        return current_input
    
    #Abstract method
    def push(self, inp):
        self._value[''] = inp
    
class Inputable(TkIO):
    def __init__(self, *args):
        super().__init__(*args)
        self.ready_flag = False
        
    @property
    def value(self):
        if self.ready_flag:
            return self.value['']
        else:
            return None
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
    
    def ready(self):
        self.ready_flag = True
        
    def unready(self):
        self.ready_flag = False
    
    
class Outputable(TkIO):
    def __init__(self, *args):
        super().__init__(*args)
        self.outputs = []
        
    def bind(self, io_object, transform=id):
        assert isinstance(io_object, Outputable)
        self.outputs.append(io_object, transform)
    
    def bind_to(self, io_object, transform=id):
        assert isinstance(io_object, Outputable)
        io_object.outputs.append(self, transform)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
        self.update()
        
        for (io_obj, transform) in self.outputs:
            out = transform(inp)
            io_obj.value = out
        
    #method to update text, not all widgets will need
    def update(self):
        pass
    
class LabelBox(Inputable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        def text_start(e):
            self.unready()
            
        def text_finish(e):
            self.value = self.box.get()
            self.ready()
                
        text = kwargs.get('text', '')
        self.text = ttk.Label(self, text=text, relief='solid') 
        self.box = ttk.Entry(self, exportselection=0)
        
        self.text.pack(expand=True, fill=tk.BOTH)
        self.box.pack(expand=True, fill=tk.BOTH)
        
        self.box.bind('<FocusIn>', text_start)
        self.box.bind('<FocusOut>', text_finish)

    def pop(self):
        current_text = super().pop()
        self.box.delete(0, tk.END)
        return current_text
    
    def push(self, text):
        self.box.delete(0, tk.END)
        self.box.insert(0, text)
        self.value = text

class IOButton(Outputable):
    def __init__(self, command, *args, **kwargs):
        super().__init__(*args)
        
        self.command = command
        self.button = ttk.Button(self, command=self.run, **kwargs)
        self.button.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.value = self.command()
        
class OysterPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.brood_count_dict = {}
        def predict_brood_count():
            count, image = self.get_prediction()
            self.brood_count_dict[self.image_pointer] = count
            self.set_prediction_image(self.image_pointer, image)
            return count
        
        self.add_input(LabelBox, text='Group Number')
        self.add_input(LabelBox, text='Size Class')
        self.add_input(LabelBox, text='Seed Tray Weight (g)')
        self.add_input(LabelBox, text='Slide Weight (g)')
        self.add_input(LabelBox, text='Slide + Seed Weight (g)')
        
        predict_button = self.add_settings(IOButton, text='Predict Brood Count', command=self.get_prediction_count)
        self.add_settings(ttk.Button, text='Load Data from Excel')
        self.add_settings(ttk.Button, text='Export to Excel')
    
    #TODO: Implement get_prediction
    def get_prediction_count(self):
        return 0
    
    def get_prediction_image(self):
        return self.black_photoimage
    
if __name__ == '__main__':
    root = tk.Tk()
    oyster = OysterPage(root)
    style_obj = Style(theme='darkly')
    
    oyster.grid(row=0, column=0, sticky='NSEW')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    #root.maxsize(1400, 800)
    root.mainloop()
