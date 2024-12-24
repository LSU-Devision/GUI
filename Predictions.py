from csbdeep.utils import normalize
from PIL import Image
from skimage.measure import find_contours
from Slideshow import Slideshow
from stardist import random_label_cmap
from tkinter import messagebox, ttk
import datetime
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import tensorflow as tf
import threading
import time
import tkinter as tk
import Utilities as utils
matplotlib.use('agg')

FROG_EGG_COUNTER = "models\\frog-egg-counter"
OYSTER_SEED_COUNTER = "models\\Oyster_model"
FROG_EGG_CLASSIFICATION = "models\\Xenopus Frog Embryos Classification Model"
class Predictions:
    def __init__(self, image_files, parent):
        self.image_files = image_files
        self.master = parent
        self.device = '/GPU:0' if tf.config.experimental.list_physical_devices('GPU') else '/CPU:0'
        # self.model = model
        self.lbl_cmap = random_label_cmap()
        self.predictions_data = []
        self.prediction_files = {}
        self.predict_index = 1
        self.settings = self.master.settings
        self.slideshow = self.master.slideshow

    def get_model_classes(self):
        config_file_path = f"{self.master.model_path}/config.json"
        with open(utils.resource_path(config_file_path), 'r') as file:
            config_data = json.load(file)
            n_classes = config_data.get('n_classes')
        return n_classes
    
    def get_model_channels(self):
        config_file_path = f"{self.master.model_path}/config.json"
        with open(utils.resource_path(config_file_path), 'r') as file:
            config_data = json.load(file)
            n_channel = config_data.get('n_channel_in')
        return n_channel

    def _predict_count(self, image_path, i):
        img = Image.open(image_path)
        
        if self.get_model_channels() == 1:
            if img.mode != 'L':
                img = img.convert('L')
        
        if self.get_model_channels() == 3:
            if img.mode == 'RGBA':
                img = img.convert('RGB')
        
        img = np.array(img)
        img = normalize(img, 1, 99.8, axis=(0,1))
        # set's predict index to the length of predictions data + 1
        self.predict_index = len(self.predictions_data) + 1
        with tf.device(self.device):
            labels, details = self.model.predict_instances(img, n_tiles=self.model._guess_n_tiles(img))

        date = datetime.datetime.now().date().strftime("%Y/%m/%d")
        time = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.predictions_data.append((self.predict_index, date, time, os.path.basename(image_path), len(details['points'])))
        autosave_images = self.master.settings['toggles']['autosave-image-default']
        if autosave_images:
            fig, ax = plt.subplots(figsize=(13, 10))
            ax.imshow(img, cmap="gray")
            ax.imshow(labels, cmap=self.lbl_cmap, alpha=0.5)
            ax.set_title(f"Predicted Objects: {len(np.unique(labels)) - 1}", fontsize=16)
            ax.axis("off")
            plt.tight_layout()
            if self.master.excel_editor.get_output_folder() is None:
                self.master.excel_editor.set_output_folder('output')
            save_path = os.path.join(self.master.excel_editor.get_output_folder(), f'prediction_{os.path.basename(image_path)}')
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            fig.savefig(save_path, dpi=500)
            plt.close(fig)

            self.prediction_files[image_path] = (save_path, len(details['points']))
        else:
            self.prediction_files[image_path] = (None, len(details['points']))

    # Function to extract class information from the prediction result
    def class_from_res(self, res):
        cls_dict = dict((i+1,c) for i,c in enumerate(res['class_id']))
        return cls_dict

    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']

    def _predict_class(self, image_path, i):
        img = Image.open(image_path)
        original = img

        if self.get_model_channels() == 1:
            if img.mode != 'L':
                img = img.convert('L')
        
        if self.get_model_channels() == 3:
            if img.mode == 'RGBA':
                img = img.convert('RGB')

        img = np.array(img)
        img = normalize(img, 1, 99.8, axis=(0,1))
        
        labels, results = self.model.predict_instances(img, n_tiles = self.model._guess_n_tiles(img))

        date = datetime.datetime.now().date().strftime("%Y/%m/%d")
        time = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.predictions_data.append((self.predict_index, date, time, os.path.basename(image_path), len(results['points'])))
        self.predict_index += 1

        autosave_images = self.master.settings['toggles']['autosave-image-default']
        print(f'settings is : {autosave_images}')
        if autosave_images:



            # Extract counts and key/value pairs from the labels image
            unique_labels, counts = np.unique(labels, return_counts=True)
            label_counts = dict(zip(unique_labels, counts))

            # Remove the background label (assumed to be 0)
            if 0 in label_counts:
                del label_counts[0]

            # Extract classes if available
            cls_dict = self.class_from_res(results)

            class_counts = {}
            if cls_dict:
                for key, value in cls_dict.items():
                    if value == 0:
                        continue
                    if value in class_counts:
                        class_counts[value] += 1
                    else:
                        class_counts[value] = 1

            # Create the class count string for the title in ascending order
            class_counts_str = ", ".join(f"Class {k}: {v}" for k, v in sorted(class_counts.items()))

            # Calculate the number of predicted objects based on the class counts
            num_objects = sum(class_counts.values())


            # Initialize a plot of specified size
            fig, ax = plt.subplots(figsize=(13, 10))
            ax.imshow(original)
            #ax.imshow(labels, cmap=self.lbl_cmap, alpha=0.25)

            # Find contours for each label and plot them with the respective class color
            for region in np.unique(labels):
                if region == 0:
                    continue
                class_id = cls_dict.get(region, 0)
                color = self.colors[class_id % len(self.colors)]  # Select color based on class ID
                contours = find_contours(labels == region, 0.5)
                for contour in contours:
                    ax.plot(contour[:, 1], contour[:, 0], linewidth=2, color=color)
    
            ax.set_title(f"Predicted Objects: {num_objects}\n({class_counts_str})", fontsize=16)
            ax.axis("off")

            # Adjust subplot parameters to remove extra whitespace
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.tight_layout(pad=0)

            save_path = os.path.join(self.master.excel_editor.get_output_folder(), f'prediction_{os.path.basename(image_path)}')
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            fig.savefig(save_path, dpi=500, bbox_inches='tight', pad_inches=0)
            plt.close(fig)

            self.prediction_files[image_path] = (save_path, len(results['points']))
        else:
            self.prediction_files[image_path] = (None, len(results['points']))

    def predict_all(self):
        threading.Thread(target=self.thread_predict_all).start()
        self.master.disable_button(self.master.predict_all_button)

    def thread_predict_all(self):
        self.create_progress_popup()

        total_images = len(self.image_files)
        start_time = time.time()
        self.progress_bar['maximum'] = total_images
        self.progress_bar['value'] = 0
        self.predicted_images_label.config(text=f'Predicted 0/{total_images} images')
        self.estimated_time_label.config(text='Estimated time remaining: Calculating...')

        for i, self.image_path in enumerate(self.image_files):
            if self.get_model_classes() == None:
                self._predict_count(self.image_path, i)
            else:
                self._predict_class(self.image_path, i)
            elapsed_time = time.time() - start_time
            avg_time_per_image = elapsed_time / (i + 1)
            remaining_time = int(avg_time_per_image * (total_images - (i + 1)))

            print(f"Predicted {i + 1}/{total_images} images. Estimated time remaining: {remaining_time} seconds")
            self.progress_bar.after(0, self.update_progress, i + 1, total_images, remaining_time)

        self.predict_index = 1
        if self.master.automatic_excel_setting:
            self.master.excel_editor.export_predictions_to_excel()
        self.master.slideshow.update_image()
        self.master.oyster_slideshow.update_image()
        total_elapsed_time = int(time.time() - start_time)
        print(f"Predicted {total_images} images in {total_elapsed_time} seconds")
        self.progress_bar.after(0, self.show_completion_message, total_images, total_elapsed_time)
        self.master.enable_button(self.master.predict_all_button)

    def create_progress_popup(self):
        self.progress_popup = tk.Toplevel(self.master)
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

    def get_model_path(self, option):
        """
        method: get_model_path
        description: returns the path to the model selected by the user
        :param option: option that the user selected
        :return: string of the path to the model
        """
        if option == 'Frog Egg Counter':
            return utils.resource_path(FROG_EGG_COUNTER)
        elif option == 'Oyster Seed Counter':
            return utils.resource_path(OYSTER_SEED_COUNTER)
        elif option == 'Frog Egg Classification':
            return utils.resource_path(FROG_EGG_CLASSIFICATION)
        else:
            messagebox.showerror("Error", "Invalid model selected")