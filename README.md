# LSU DeVision
Official Github  
Framework created by [Jeffrey Tepper](https://github.com/jeffreytepper)

## Raspberry Pi Camera Support
If you are running this application on a Raspberry Pi and want to use the Pi camera, you must install the `picamera2` package manually:

```bash
pip install picamera2
```

This step is only required for Raspberry Pi users who want to use the Pi camera. On other systems, only `opencv-python` is required for webcam support.

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
