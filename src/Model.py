from stardist.models import StarDist2D
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
import os
import json
from matplotlib import pyplot as plt
from csbdeep.utils import normalize


#### Training TUI
class AnnotatedLoader():
    def __init__(self,
                 image_dir=Path('annotated-images') / Path('alloted-images'),
                 csv_dir = Path('annotated-images') / Path('csv-files'),
                 from_csv=True,
                 memory_limit=64):
        
        self.image_dir = image_dir
        self.csv_dir = csv_dir
        self.from_csv = from_csv
        self.memory_limit = memory_limit
        
        self.image_paths = list(map(lambda x: str(self.image_dir / Path(x)),
                                    os.listdir(self.image_dir)))
                
        self.image_len = (0, min(self.memory_limit, len(self.image_paths)))
        
        self.images = {}
        self.labels = {}
        
        self._load_images()
        
    def _load_images(self):
        for index in range(*self.image_len):
            name = self.image_paths[index]
            
            with Image.open(name) as img:
                img_rgb = img.convert('L')
                self.images[name] = np.array(img_rgb)
            
                if self.from_csv:
                    csv_path = self.csv_dir / Path(name).with_suffix('.csv').name
                    label = self._csv_to_label_mask(csv_path, img.size)
                    self.labels[name] = label
                
    def _csv_to_label_mask(self, path, img_size):
        mask = Image.new(mode='1', size=img_size, color=0)
        canvas = ImageDraw.Draw(mask, mode='1')
        
        data = pd.read_csv(path)['region_shape_attributes'].to_list()
        for shape in data:
            shape = json.loads(shape)
            if shape['name'] == 'circle':
                canvas.circle(xy=(shape['cx'], shape['cy']), radius=shape['r'], fill=1, outline=1)
            else:
                raise ValueError('Shape not a circle, please implement non circular shapes in this code')

        return np.array(mask)
    
    def data(self):
        for index in range(len(self.image_paths)):
            name = self.image_paths[index]
            
            if len(self.images) == 0 and index != len(self.image_paths) - 1:
                self.image_len = (self.image_len[1]+1, min(self.image_len[1] + self.memory_limit, len(self.image_paths) - self.image_len[1]))
                self._load_images()
            
            yield self.images.pop(name), self.labels.pop(name)

dataset = AnnotatedLoader().data()

if __name__ == '__main__':
    
    train = False
    
    if train:
        model = StarDist2D(name='empty-model', basedir='test/model')
        model.prepare_for_training()

        X_train = []
        y_train = []
        for _ in range(10):
            X, y = next(dataset)
            X_train.append(X)
            y_train.append(y)
            
        X_val = []
        y_val = []
        for _ in range(5):
            X, y = next(dataset)
            X_val.append(X)
            y_val.append(y)
        
    else:
        model = StarDist2D(config=None, name='empty-model', basedir='test/model')
   
    X_test = []
    y_test = []
    for _ in range(5):
        X, y = next(dataset)
        X_test.append(X)
        y_test.append(y)
    
    if train:
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        X_val = np.array(X_val)
        y_val = np.array(y_val)    
        
        print('Model is training...')
        history = model.train(X_train, y_train, validation_data=(X_val, y_val), epochs=1, steps_per_epoch=X_train.shape[0])
        print('Model done training!')
    
        pd.DataFrame(history.history).plot(figsize=(8,5))
        plt.show()
       
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    
    
    print('Model is predicting...')
   
    img = normalize(X_test[0], 1, 99.8, axis=(0,1))
    y_pred = model.predict_instances(img)
    
    print('Model done predicting!')
    
    print(y_pred)