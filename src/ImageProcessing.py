from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage
from pathlib import Path
import json
import os
import numpy as np
from functools import reduce
from matplotlib import pyplot as plt

THUMBNAIL_SIZE = (400, 400)
DARKBLUE = (0, 0, 75)
class ImageList(list):
    def __init__(self, name, iterable=[]):
        """Listlike object that contains paths and image references, but appends via image path for convienience
           Use ImageList().paths to access the underlying path objects
            *args: Iterable of path-like objects
            
        """
        self.name = name
        
        self.black_photoimage = PhotoImage(Image.new(mode='RGB', color=(0, 0, 0), size=THUMBNAIL_SIZE))
        self.paths = []
        images = []
        for path in iterable:
            path, image = self._process_path(path)
            self.paths.append(path)
            images.append(image)
        
        super().__init__(images)
        self._json_dump()
    
    def __setitem__(self, key, value):
        path, image = self._process_path(value)
        self.paths[key] = path
        super().__setitem__(key, image)
        self._json_dump()

    def __delitem__(self, key):
        del self.paths[key]
        return_value = super().__delitem__(key)
        self._json_dump()
        return return_value
    
    def extend(self, iterable):
        paths = []
        images = []
        for path in iterable:
            path, image = self._process_path(path)
            paths.append(path)
            images.append(image)
            
        self.paths.extend(paths)
        super().extend(images)
        self._json_dump()

    def append(self, path):
        path, image = self._process_path(path)
        self.paths.append(path)
        super().append(image)
        self._json_dump()
    
    def _process_path(self, path):
        if path == None or path == 'None':
            return None, self.black_photoimage
        
        path = Path(path).resolve()
        image = Image.open(path)
        image_copy = PhotoImage(image.resize(THUMBNAIL_SIZE))
        image.close()
        
        return path, image_copy
   
    def _json_dump(self):
        str_paths = list(map(lambda x: str(x), self.paths))
        cwd = Path(os.getcwd())
        file_path = cwd / Path('config') / Path(f'ImageList{self.name}.json')
        
        
        with open(file_path, 'w') as file:
            json.dump(obj=str_paths, fp=file, indent=2)

def highlight_boundary(img: Image.Image, mask: Image.Image, color, width=1):
    """_summary_

    Args:
        img (_type_): _description_
    """
    mask_arr = np.asarray(mask, dtype=np.uint8)

    right_arr = np.roll(mask_arr, shift=1, axis=0)
    left_arr = np.roll(mask_arr, shift=-1, axis=0)
    up_arr = np.roll(mask_arr, shift=1, axis=1)
    down_arr = np.roll(mask_arr, shift=-1, axis=1)
    
    shifts = [right_arr, left_arr, up_arr, down_arr]
    xor_shifts = list(map(lambda x: np.logical_xor(x, mask_arr), shifts))
    
    boundary = reduce(lambda x, y: np.logical_or(x, y), xor_shifts)
    for roll in range(width - 1):
        right_arr = np.roll(boundary, shift=1, axis=0)
        left_arr = np.roll(boundary, shift=-1, axis=0)
        up_arr = np.roll(boundary, shift=1, axis=1)
        down_arr = np.roll(boundary, shift=-1, axis=1)
        shifts = [right_arr, left_arr, up_arr, down_arr]
        boundary = reduce(lambda x, y: np.logical_or(x, y), shifts, boundary)
    
    
    color_img = Image.new(mode='RGB', size=img.size, color=color)
    
    boundary_img = Image.new(mode='1', size=mask.size)
    boundary_img.putdata(boundary.flatten())
    
    highlighted_img = img.copy()
    highlighted_img.paste(color_img, box=(0, 0), mask=boundary_img)
    
    
    
    return highlighted_img
    
        
if __name__ == '__main__':
    mask = Image.new(mode='1', size=(400, 400), color=0)
    img = Image.new(mode='RGB', size=(400, 400), color=(0, 0, 0))
    canvas = ImageDraw.Draw(img, mode='RGB')
    canvas.rectangle(((200, 200), (250, 250)), fill=(155, 0, 0), )
    
    canvas_mask = ImageDraw.Draw(mask, mode='1')
    canvas_mask.circle((200, 200), radius=20, fill=1)
    
    
    plt.imshow(highlight_boundary(img, mask, DARKBLUE, width=4))
    plt.show()