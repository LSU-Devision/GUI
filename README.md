# LSU DeVision
Official Github  
Framework created by [Jeffrey Tepper](https://github.com/jeffreytepper)

## Table of Contents
- [Building an Executable](#building-an-executable)
- [Raspberry Pi Setup](#raspberry-pi-setup)

## Building an Executable
To build an executable on your target system:

### Prerequisites
1. Ensure the code compiles and runs correctly:
   ```bash
   python src/Pages.py
   ```

2. First-time setup: Install PyInstaller if not already installed:
   ```bash
   pip install pyinstaller
   ```

### Building Process
1. Generate the executable using the spec file:
   ```bash
   pyinstaller DeVision.spec
   ```
   This will output the executable into the `dist/` folder.

2. Make the file executable (Linux/Mac only):
   ```bash
   chmod +x ./dist/DeVision
   ```

### Testing
Test the executable by either:
- Running it from the command line:
  ```bash
  ./dist/DeVision
  ```
- Double-clicking the executable icon

### Distribution
Once you've verified the program runs successfully, compress it into a zip file and replace the old distribution in the GitHub repository.

## Raspberry Pi Setup

### Raspberry Pi Camera Support
If you are running this application in development mode (not using the pre-built executable) on a Raspberry Pi and want to use the Pi camera, you must install the `picamera2` package manually:
```bash
pip install picamera2
```
This step is only required for Raspberry Pi users who want to use the Pi camera. On other systems, only `opencv-python` is required for webcam support.

### Hardware Requirements
* Raspberry Pi 5 (>=8GB recommended)
* Active or Passive cooling system for Raspberry Pi - [Example](https://vilros.com/products/raspberry-pi-5-active-cooler)
* Micro SD card (>=32GB recommended)
* Raspberry Pi native camera (Raspberry Pi AI Camera recommended)
   * Note: You can use any Raspberry Pi camera or USB camera, but the casing was designed specifically for the Pi AI/Module 2 cameras
* Raspberry Pi 7" touchscreen display
* 3D printed housing (see attached files)
   * Requires 4-40 x ¼ screws (x8) for assembly
* Portable Battery Solution:
   * ~65W USB-C Power Delivery Power Bank 
      * Needed for stable 5V/5A output for the Pi 5 during mobile operation
   * Power Cable:
      * 100W USB-C to USB-C Cable with E-marker (5A Rated)

Note: For ease of setup, we recommend having a USB keyboard, mouse, and flash drive

### Hardware Setup Tutorial 
* video link: https://youtu.be/5IRF50kIswU

### Camera Setup
1. Connect to WiFi
2. Install updates for Raspberry Pi Software 
3. Install software needed to use the Raspberry Pi camera:
   ```bash
   sudo apt update && sudo apt full-upgrade
   sudo apt install imx500-all
   sudo reboot
   ```
   For more information, see: [Raspberry Pi Camera Documentation](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)
4. Download the DeVision program to the Raspberry Pi (recommended location: Desktop)
5. Run the DeVision Program:
   * Method 1: Double-click the DeVision program
   * Method 2: Open terminal and run:
     ```bash
     ./your/path/DeVision
     ```

### Design Suggestions for 3D Printed Housing
* [7-inch-display-mechanical-drawing](https://datasheets.raspberrypi.com/display/7-inch-display-mechanical-drawing.pdf)
* Recommend adding a front lip for the screen to avoid scratches
* Camera housing orientation needs to be rotated 90° to align camera orientation with display screen
* Look into better placement for cable management
* Need to add housing for the battery pack:
   * Recommended placement is along the base of the screen intersecting casing at a 10-30 degree angle
   * This allows the battery to double as a base/stand for the Pi
* Fill unused cooling holes and ports (to prevent water/dust damage)
