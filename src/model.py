from stardist.models import StarDist2D
from pathlib import Path
from PIL import Image
import numpy as np
from csbdeep.utils import normalize
import os
from importlib import import_module
import pandas as pd
from image_processing import highlight_boundary

def count_by_class(class_arr):
    class_dict = {}
    for class_id in class_arr:
        class_dict[class_id] = class_dict.get(class_id, 0) + 1
    return class_dict

class ModelAPI:
    def __init__(self, 
                 model_dir: os.PathLike,
                 img: Image.Image,
                 classes: int=1):
        """StarDist2D Prediction wrapper, provides methods to return object count and create an annotated PIL image from model outputs

        Args:
            model_dir (os.PathLike): The directory containing the .config file for the stardist model 
            img (PIL.Image.Image): The image the prediction is being run on
            classes (int): The number of predicted classes the stardist model is set to run on, defaults to 1.
        """        
        
        model_dir = Path(model_dir)
        
        # If we're running as a bundled app, check for environment variable path
        if getattr(import_module('sys'), 'frozen', False) and os.environ.get('DEVISION_MODELS'):
            # If the model_dir is a relative path starting with 'models', use the environment variable
            if str(model_dir).startswith('models'):
                # Extract the subdirectory path after 'models/'
                subdir = str(model_dir).split('models/', 1)[1] if 'models/' in str(model_dir) else ''
                model_dir = Path(os.environ.get('DEVISION_MODELS')) / subdir
                print(f"Using bundled model path: {model_dir}")
        
        basedir = model_dir.parent
        name = model_dir.stem
        
        try:
            self._model = StarDist2D(
                config=None,
                basedir=basedir,
                name=name
            )
        except Exception as e:
            print(f"Error loading model from {model_dir}: {str(e)}")
            # Print directory content to help with debugging
            print(f"Directory exists: {os.path.exists(basedir)}")
            if os.path.exists(basedir):
                print(f"Files in {basedir}: {os.listdir(basedir)}")
            raise
        
        # Resize the image if the resolution is incorrect
        if img.size != (3024, 4032):
            img = img.resize(3024, 4032)
        
        self._image = img
        self._nclasses = classes
        
        if self._model.config.n_channel_in == 3:
            img = img.convert('RGB')
        elif self._model.config.n_channel_in == 1:
            img = img.convert('L') 
        
        img_arr = np.array(img)
        # Ensure the array is always 3D (H, W, C)
        if img_arr.ndim == 2:
            img_arr = np.expand_dims(img_arr, axis=-1)
        self._arr = normalize(img_arr, 1, 99.8, axis=(0, 1))
        self._prediction_flag = False
        
        self._count = None
        self._out_image = None
        
    def _predict(self):
        n_tiles = self._model._guess_n_tiles(self._arr)
        lbls, details = self._model.predict_instances(self._arr, n_tiles=n_tiles, axes='YXC')
        
        if self._nclasses > 1:
            class_dct = {k+1:v for k, v in enumerate(details['class_id'])}
        else:
            class_dct = {k+1:1 for k in range(len(details['points']))}
            
        mask_image = Image.new(mode='L', color=0, size=self._image.size)
        mask_image.putdata(lbls.flatten())
        
        self._count = len(details['points'])
        
        if 'class_id' in details:
            self.count_dct = count_by_class(details['class_id'])
        else:
            self.count_dct = {}
            
        self.color_dct = {
            1: 'red',
            2: 'blue',
            3: 'green',
            4: 'yellow'
        }
        
        self._out_image = highlight_boundary(self._image, mask_image, width=4, classes=self._nclasses, class_dct=class_dct, colors=self.color_dct)

    def df(self):
        
        
        data_lst = [str(self._image_path.name), 
                    self._count] + [self.count_dct.get(i, 0) for i in range(4)]
        
        df = pd.DataFrame([data_lst], 
                     columns=['File', 
                              'Total Count', 
                              'Nonviable Count (Red)', 
                              'Two-Split Count (Blue)', 
                              'Four-Split Count (Green)', 
                              'Eight-Split Count (Yellow)']
                     )
        return df
    
    def get(self):
        if self._count is None or self._out_image is None:
            self._predict()
        return self._count, self._out_image