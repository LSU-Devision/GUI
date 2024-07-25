import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tensorflow as tf
import os.path
import numpy as np
from csbdeep.utils import normalize
from PIL import Image
from stardist.models import StarDist2D
from tkinter import messagebox
import csv
import datetime
import time
import threading
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from stardist import random_label_cmap
from Slideshow import Slideshow
import Settings
import Utilities as utils
from openpyxl import Workbook, load_workbook
import MainFrame

class Predictions:
    def __init__(self, image_files, parent, model, main_frame):
        self.image_files = image_files
        self.parent = parent
        self.device = '/cpu:0'  # Update this based on your device configuration
        # self.model = model
        self.lbl_cmap = random_label_cmap()
        self.predictions_data = []
        self.prediction_files = {}
        self.predict_index = 1
        self.settings = Settings.SettingsJson()
        self.slideshow = Slideshow(self.parent)
        self.mainframe = main_frame

    def _predict(self, image_path):
        img = Image.open(image_path)
        if img.mode != 'L':
            img = img.convert('L')
        
        img = np.array(img)
        img = normalize(img, 1, 99.8, axis=(0,1))

        with tf.device(self.device):
            labels, details = self.model.predict_instances(img, n_tiles=self.model._guess_n_tiles(img))
        date = datetime.datetime.now().date().strftime("%Y/%m/%d")
        time = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.predictions_data.append((self.predict_index, date, time, os.path.basename(image_path), len(details['points'])))
        self.predict_index += 1

        if self.settings.get_save_images_output():
            fig, ax = plt.subplots(figsize=(13, 10))
            ax.imshow(img, cmap="gray")
            ax.imshow(labels, cmap=self.lbl_cmap, alpha=0.5)
            ax.set_title(f"Predicted Objects: {len(np.unique(labels)) - 1}", fontsize=16)
            ax.axis("off")
            plt.tight_layout()
            save_path = os.path.join('output', f'prediction_{os.path.basename(image_path)}')
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            fig.savefig(save_path, dpi=500)
            plt.close(fig)
            self.prediction_files[image_path] = (save_path, len(details['points']))
        else:
            self.prediction_files[image_path] = (None, len(details['points']))

    def predict_all(self):
        threading.Thread(target=self.thread_predict_all).start()
        self.mainframe.disable_button(self.mainframe.predict_all_button)

    def thread_predict_all(self):
        self.create_progress_popup()

        total_images = len(self.image_files)
        start_time = time.time()
        self.progress_bar['maximum'] = total_images
        self.progress_bar['value'] = 0
        self.predicted_images_label.config(text=f'Predicted 0/{total_images} images')
        self.estimated_time_label.config(text='Estimated time remaining: Calculating...')

        for i, self.image_path in enumerate(self.image_files):
            self._predict(self.image_path)
            elapsed_time = time.time() - start_time
            avg_time_per_image = elapsed_time / (i + 1)
            remaining_time = int(avg_time_per_image * (total_images - (i + 1)))

            print(f"Predicted {i + 1}/{total_images} images. Estimated time remaining: {remaining_time} seconds")
            self.progress_bar.after(0, self.update_progress, i + 1, total_images, remaining_time)

        self.predict_index = 1
        if self.mainframe.settings.get_automatic_csv_export():
            self.mainframe.excel_editor.export_predictions_to_csv()
        self.mainframe.slideshow.update_image()
        total_elapsed_time = int(time.time() - start_time)
        print(f"Predicted {total_images} images in {total_elapsed_time} seconds")
        self.progress_bar.after(0, self.show_completion_message, total_images, total_elapsed_time)
        self.mainframe.enable_button(self.mainframe.predict_all_button)

    def create_progress_popup(self):
        self.progress_popup = tk.Toplevel(self.parent)
        self.progress_popup.title("Prediction Progress")

        self.progress_bar = ttk.Progressbar(self.progress_popup, orient='horizontal', mode='determinate', length=300)
        self.predicted_images_label = ttk.Label(self.progress_popup, text='Predicted 0/0 images')
        self.estimated_time_label = ttk.Label(self.progress_popup, text='Estimated time remaining: N/A')

        self.progress_bar.grid(row=0, column=0, pady=5)
        self.predicted_images_label.grid(row=1, column=0, pady=5)
        self.estimated_time_label.grid(row=2, column=0, pady=5)

    def update_progress(self, current, total, remaining_time):
        if self.progress_popup and self.progress_popup.winfo_exists():
            self.progress_bar['value'] = current
            self.predicted_images_label.config(text=f'Predicted {current}/{total} images')
            self.estimated_time_label.config(text=f'Estimated time remaining: {remaining_time} seconds')
            self.progress_popup.update_idletasks()

    def show_completion_message(self, total_images, total_elapsed_time):
        if self.progress_popup and self.progress_popup.winfo_exists():
            messagebox.showinfo("Prediction Complete", f"Predicted {total_images} images in {total_elapsed_time} seconds")
            self.estimated_time_label.config(text='Estimated time remaining: N/A')
            self.predicted_images_label.config(text=f'Predicted {total_images}/{total_images} images')
            self.progress_bar['value'] = 0
            self.progress_popup.destroy()
