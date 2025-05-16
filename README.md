# LSU DeVision
Official Github  
Framework created by [Jeffrey Tepper](https://github.com/jeffreytepper)

## Table of Contents
- [Building an Executable](#building-an-executable)
- [Raspberry Pi Setup](#raspberry-pi-setup)
- [Raspberry Pi Bluetooth Setup](#raspberry-pi-bluetooth-file-transfer-setup-guide)

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
* 3D printed housing ([see attached files](https://github.com/LSU-Devision/GUI/tree/main/3d-raspberry-pi-housing))
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

## Raspberry Pi Bluetooth File Transfer Setup Guide

This feature allows transferring photos from a smartphone (iOS or Android) to the Raspberry Pi using Bluetooth, without needing WiFi or physical connections. The GUI application can then process these received photos.

### Prerequisites

*   Raspberry Pi (Raspberry Pi 5 recommended) with Raspberry Pi OS installed.
*   Bluetooth capability (built into Raspberry Pi 3 and later models).
*   iOS or Android smartphone with Bluetooth capability.
*   Admin (sudo) access to your Raspberry Pi.

### Installation and Setup Steps

1.  **Update Your System**:
    Open a terminal on your Raspberry Pi and run:
    ```bash
    sudo apt update
    sudo apt upgrade -y
    ```

2.  **Install Required Packages**:
    Install BlueZ (Bluetooth protocol stack), tools, and Python Flask (for the web server):
    ```bash
    sudo apt install bluez bluez-tools python3-flask -y
    ```

3.  **Configure Bluetooth Visibility and Pairing**:
    Make your Raspberry Pi discoverable and pairable. Open a terminal and run `sudo bluetoothctl`, then enter the following commands one by one:
    ```bash
    power on
    discoverable on
    pairable on
    agent on
    default-agent
    quit
    ```
    These settings ensure your phone can find and pair with the Raspberry Pi.

4.  **Set Up Bluetooth Personal Area Network (PAN)**:
    This allows your phone to create a network connection with the Raspberry Pi over Bluetooth.

    *   Create a systemd service file for the PAN server:
        ```bash
        sudo nano /etc/systemd/system/bt-pan.service
        ```
    *   Add the following content to this file:
        ```
        [Unit]
        Description=Bluetooth Personal Area Network
        After=bluetooth.service
        PartOf=bluetooth.service

        [Service]
        ExecStart=/usr/bin/bt-network -s nap
        Type=simple

        [Install]
        WantedBy=bluetooth.target
        ```
        Save the file and exit nano (Ctrl+X, then Y, then Enter).

    *   Enable and start the service:
        ```bash
        sudo systemctl enable bt-pan.service
        sudo systemctl start bt-pan.service
        ```
    *   To check its status:
        ```bash
        sudo systemctl status bt-pan.service
        ```

5.  **File Transfer Server Script (`bt_file_server.py`)**:
    The GUI application includes a Python script named `bt_file_server.py` (located in the project root). This script runs a simple Flask web server that your phone connects to (via its web browser, over the Bluetooth PAN connection) to upload photos.

    *   Ensure this script is executable. If you cloned the repository or downloaded it, it should have the correct permissions. If not, you can set it from the project root directory:
        ```bash
        chmod +x bt_file_server.py
        ```

### Using the Feature in the GUI

1.  **Pair Your Phone**: Ensure your smartphone is paired with your Raspberry Pi via Bluetooth standard pairing procedures.
2.  **Launch the GUI Application**: Run the DeVision application.
3.  **Initiate Reception**: In the GUI, click the "Receive via Bluetooth" button or by clicking the blutooth icon on the top right.
4.  **Follow GUI Instructions**: The application will display a message with the Raspberry Pi's IP address (accessible over the Bluetooth PAN) and port (e.g., `http://<IP_ADDRESS>:5000`).
5.  **Upload from Phone**: On your phone, open a web browser and navigate to the address provided by the GUI.
6.  **Select and Upload**: Use the web page on your phone to select and upload a photo.
7.  **Automatic Processing**: Once uploaded, the photo will be saved to the `~/bluetooth_transfers/` directory on the Raspberry Pi, and the GUI will automatically detect and load it for processing.

### Troubleshooting

*   **Bluetooth Not Connecting/PAN not working**: 
    *   Ensure your phone and Pi are paired.
    *   Verify the `bt-pan.service` is active: `sudo systemctl status bt-pan.service`.
    *   Restart Bluetooth services if needed: `sudo systemctl restart bluetooth`.
    *   On some phones, you might need to explicitly enable Bluetooth tethering or PAN connection after pairing.
    *   Make sure the Pi and Phone are connected to the same WiFi / Personal Hotspot
*   **Cannot Access Web Interface on Phone**: 
    *   Double-check the IP address displayed by the GUI matches what you entered in the phone's browser.
    *   Ensure the `bt_file_server.py` script is running (the GUI starts it; check the terminal output where the GUI was launched for any errors from the script).
*   **Files Not Appearing in GUI**: 
    *   Check if files are present in the `~/bluetooth_transfers/` directory on the Raspberry Pi.
    *   Ensure the GUI has permissions to read from this directory (though it typically runs as the user who owns their home directory).

### Security Note

This Bluetooth transfer system is designed for local, direct transfers. It does not implement strong security measures beyond standard Bluetooth pairing. Use it on trusted networks and with trusted devices.
