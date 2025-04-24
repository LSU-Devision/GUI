from stardist.models import StarDist2D
from pathlib import Path
from PIL import Image
import numpy as np
from csbdeep.utils import normalize
import os

from ImageProcessing import highlight_boundary

### Stardist API

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
        
        basedir = model_dir.parent
        name = model_dir.stem
        
        self._model = StarDist2D(
            config=None,
            basedir=basedir,
            name=name
        )
        
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
            class_dct = {}
        
        mask_image = Image.new(mode='L', color=0, size=self._image.size)
        mask_image.putdata(lbls.flatten())
        
        self._count = len(details['points'])
        self._out_image = highlight_boundary(self._image, mask_image, width=4, classes=self._nclasses, class_dct=class_dct)
        
        #yield self._count, self._out_image
    
    def get(self):
        if self._count is None or self._out_image is None:
            self._predict()
        return self._count, self._out_image