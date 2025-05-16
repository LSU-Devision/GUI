#!/usr/bin/env python3

from flask import Flask, request, render_template_string, redirect
import os
import datetime
import subprocess
import re

app = Flask(__name__)

# Create directory for received files
save_path = os.path.expanduser("~/bluetooth_transfers")
os.makedirs(save_path, exist_ok=True)

# Get Bluetooth MAC address
my_address = "unknown"
try:
    bt_info = subprocess.check_output(["hciconfig"], universal_newlines=True)
    mac_match = re.search(r"([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})", 
                      bt_info, re.IGNORECASE)
    if mac_match:
        my_address = mac_match.group(1).lower()
except Exception:
    # hciconfig might not be available or fail, keep my_address as "unknown"
    pass


# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Raspberry Pi Photo Upload</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
        .upload-btn { background: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        #status { margin-top: 20px; }
    </style>
</head>
<body>
    <h2>Upload Photo to Raspberry Pi</h2>
    
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="photo" accept="image/*" capture>
        <button type="submit" class="upload-btn">Upload</button>
    </form>
    
    <div id="status">{{ message }}</div>
    
    <p>Upload directory: {{ save_path }}</p>
    <p>Bluetooth MAC: {{ bt_mac }}</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, message='', save_path=save_path, bt_mac=my_address)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return render_template_string(HTML_TEMPLATE, message='No file part', save_path=save_path, bt_mac=my_address)
    
    file = request.files['photo']
    
    if file.filename == '':
        return render_template_string(HTML_TEMPLATE, message='No file selected', save_path=save_path, bt_mac=my_address)
    
    if file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize filename to prevent path traversal issues if ever needed, though os.path.join helps
        safe_filename = os.path.basename(file.filename)
        filename = os.path.join(save_path, f"{timestamp}_{safe_filename}")
        file.save(filename)
        print(f"File received and saved as {filename}") # Log to server console
        return render_template_string(HTML_TEMPLATE, 
                                   message=f'File uploaded successfully!', # Simplified message
                                   save_path=save_path,
                                   bt_mac=my_address)

def get_ip_address():
    try:
        ip_info = subprocess.check_output(["hostname", "-I"], universal_newlines=True).strip()
        # Return the first IP address if multiple are listed
        return ip_info.split(' ')[0]
    except Exception:
        return None

if __name__ == '__main__':
    ip_address = get_ip_address()
    
    if ip_address:
        print(f"Server IP address: {ip_address}")
    else:
        print("Could not determine IP address. Ensure 'hostname -I' works.")
        
    print(f"Bluetooth MAC address: {my_address}")
    print(f"Starting web server for file uploads on port 4020.")
    print(f"Files will be saved to: {save_path}")
    print(f"Instructions for user:")
    print(f"1. Ensure your phone is paired with this Raspberry Pi via Bluetooth.")
    print(f"2. Ensure Bluetooth PAN is active on the Pi (e.g., bt-pan.service is running).")
    if ip_address:
      print(f"3. On your phone, open a web browser and go to http://{ip_address}:4020")
    else:
      print(f"3. On your phone, open a web browser and go to http://<RASPBERRY_PI_IP_ADDRESS>:4020 (check Pi's IP manually).")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=4020) 