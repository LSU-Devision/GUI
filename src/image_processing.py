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

# Helper function for path resolution
def get_data_path(relative_path: os.PathLike):
    """Helper function to get data path with environment variable support

    Args:
        relative_path (os.PathLike): The path we want to check the existence of

    Returns:
        os.PathLike: The absolute path of the data based on OS
    """
    path = Path(relative_path).absolute()

    # conditional statement to check if the path is in the data directory or if it is a child of the data directory
    # proposal, instead of checking if the data directory is at index 0, check if data is in the path.parents

    if str(path) == 'data' or (len(path.parents) > 0 and path.parents[1] == 'data'):
    #if str(path) == 'data' or (len(path.parents) > 0 and 'data' in path.parents): proposed solution
        if os.environ.get('DEVISION_DATA'):
            # If we're in a bundled app, use the environment variable path
            path = Path(path.parents[-1]) / path.name
            path = Path(os.environ.get('DEVISION_DATA')) / path
            print(f"Using bundled data path: {path}")
        
        # Make sure directory exists
        try:
            if not path.parent.exists():
                os.makedirs(path.parent)
                     
        except Exception as e:
            print(f"Warning: Error handling data path {path}: {str(e)}")
            
    return path

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
        file_path = get_data_path(f'data/ImageList{self.name}.json')
        # Ensure parent directory exists
        try:
            with open(file_path, 'w') as file:
                json.dump(obj=str_paths, fp=file, indent=2)
        except Exception as e:
            print(f"Warning: Could not save image list to {file_path}: {str(e)}")
            # Try to write to a fallback location if needed
            try:
                fallback_path = Path(f'ImageList{self.name}.json')
                print(str(fallback_path))
                with open(fallback_path, 'w') as file:
                    json.dump(obj=str_paths, fp=file, indent=2)
                print(f"Saved image list to fallback location: {fallback_path}")
            except Exception as e2:
                print(f"Failed to save image list to fallback location: {str(e2)}")

def highlight_boundary(img: Image.Image, mask: Image.Image, width=1, classes=1, class_dct={}, colors={}):
    """_summary_

    Args:
        img (_type_): _description_
    """
    class_dct.update({0:0})
    mask_arr = np.asarray(mask, dtype=np.uint8)

    f = lambda x: class_dct[x]
    f = np.vectorize(f)
    mask_arr = f(mask_arr)
        
    classes_ids = np.unique(list(class_dct.values()))
    colors_imgs = {}
    class_imgs = {}
    for i in classes_ids:
        if i == 0: continue
        mask_i = (mask_arr == i).astype(np.int32)
        colors_imgs[i] = (Image.new(mode='RGB', size=img.size, color=colors[i]))
        class_imgs[i] = mask_i
        
    highlighted_img = img.copy()

    
    for i in colors_imgs:
        mask_arr = class_imgs[i]
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
        
        boundary_img = Image.new(mode='1', size=mask.size)
        boundary_img.putdata(boundary.flatten())
        
        highlighted_img.paste(colors_imgs[i], box=(0, 0), mask=boundary_img)
    
    

    return highlighted_img
    
        
if __name__ == '__main__':
    mask = Image.new(mode='L', size=(400, 400), color=0)
    img = Image.new(mode='RGB', size=(400, 400), color=(0, 0, 0))
    canvas = ImageDraw.Draw(img, mode='RGB')
    canvas.rectangle(((200, 200), (250, 250)), fill=(155, 0, 0), )
    
    canvas_mask = ImageDraw.Draw(mask, mode='L')
    canvas_mask.circle((200, 200), radius=20, fill=1)
    canvas_mask.circle((300, 300), radius=15, fill=2)
    
    
    
    plt.imshow(highlight_boundary(img, mask, width=4, classes=2, class_dct={1:1, 2:2}))
    plt.show()