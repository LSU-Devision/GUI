# Devision User Manual

This page has a scroll bar to view the full page.

## Overview

This software uses **Stardist** models to predict object locations, number, and type contained within an input image. Our predefined models provide access to a 2-4mm seed counter as well as a 4-6mm seed counter. Our software also provides support for importing custom user-defined Stardist models with less than five classes. 

### Usage
To use this software, first import an image using the **Select an image** button, located in the top region of the page. This will open a file dialog to select an image file from your file system. Once an image has been imported into the program, it should appear in the left panel on the app page.

Select your preferred model from the model dropdown menu, located in the top center of the screen. Choosing **Select a Model from Folder** will prompt the user for a custom Stardist model *after pressing the Predict Brood Count*. This button will estimate the number of instances detected in the picture and place the result in the Model Count label located in the bottom left of the screen. While the predict button is greyed out, the program is actively calculating. Expect predictions to take ~10-30 seconds on a 2GHz CPU and predictions + annotations to take ~40-60 seconds. If the Auto-export to CSV setting is selected, this button will also output a CSV file into the default CSV directory. 

When selecting more than one image, the program will automatically place the most recent image added into the frame. To navigate back to older images, press the *Prev* (previous) and *Next* buttons to navigate. The counter in the center of the page contains the current frame integer id on the left side, and the total number of frames on the right side.

Each image frame contains a fullscreen button in the top left to see a zoomed in version of the image.

The top panel contains input boxes for calculating statistics in the CSV file. If any box is missing data, that entry in the CSV file will be skipped when exporting. The **Append to CSV file** button prompts the user for an existing CSV file in a file dialog. 

### Settings
We have a number of features that are customizable to the user. These settings are accessed by pressing on the **Settings** button. These settings will automatically reload when reentering the program. To navigate the settings window, double click or press enter on any text in the tree. The setting names are located on the left side of the settings window, and the information regarding the status of the setting (active/inactive or other relevant information) is located under the status column on the right hand side of the window. 

The following describes the settings in depth:

Defaults:
- Auto-export CSV file: Automatically export a csv file after the model prediction is done
- New CSV for predictions: Wipe all previous data contained in memory (but keep data on file) after model prediction is done.
- New CSV when clearing: Wipe all previous data contained in memory when selecting the **Clear all images** button 
- Auto-save images: Save annotated images to file in the annotations directory after predicting. If this setting is off the file will not be saved, but will appear in the program.
- Annotate predicted images: Perform annotation when predicting. Turning this option off will increase prediction speed around 3x, but will not output *any* annotated image.
- CSV Output Directory: Selecting this setting will open a file dialog prompting the user to select a new directory to automatically save CSV outputs to instead of the Excel/CSV folder.
- Annotation Output Directory: Selecting this setting will open a file dialog prompting the user to select a new directory to automatically save image outputs to instead of the Annotations folder.

**Warning**: Note that on a Docker deployment the output directory should not be changed or critical file system errors may occur. If you are running a .bat or a .sh script to run this program, this applies to you. If you are running a .exe or a compiled file for linux, this does not apply to you.

Style:
This dropdown contains a number of themes to stylize the user experience. This contains a number of built in light and dark themes, as well as a custom LSU dark theme.

Version:
This dropdown contains the check for updates button, which informs the user if a new update is avaliable and routes them to the GitHub if so.

Reset:
This dropdown contains a option that will reset all settings to their default values. This includes theme, directory options, and all toggleable options.
