#!/usr/bin/env python3

from flask import Flask, request, render_template_string, redirect
import os
import datetime
import subprocess

app = Flask(__name__)

# Create directory for received files
save_path = os.path.expanduser("~/bluetooth_transfers")
os.makedirs(save_path, exist_ok=True)

# Get Bluetooth MAC address
try:
    bt_info = subprocess.check_output(["hciconfig"], universal_newlines=True)
    import re
    mac_match = re.search(r"([0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2})", 
                      bt_info, re.IGNORECASE)
    if mac_match:
        my_address = mac_match.group(1).lower()
    else:
        my_address = "unknown"
except:
    my_address = "unknown"

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
        filename = os.path.join(save_path, f"{timestamp}_{file.filename}")
        file.save(filename)
        return render_template_string(HTML_TEMPLATE, 
                                   message=f'File uploaded successfully as {filename}',
                                   save_path=save_path,
                                   bt_mac=my_address)

if __name__ == '__main__':
    # Get IP address (will be useful for instructions)
    try:
        ip_info = subprocess.check_output(["hostname", "-I"], universal_newlines=True).strip()
        print(f"Server IP address: {ip_info}")
    except:
        print("Could not determine IP address")
        
    print(f"Bluetooth MAC address: {my_address}")
    print(f"Starting web server for file uploads")
    print(f"Files will be saved to: {save_path}")
    print(f"Use your phone to connect to this device via Bluetooth")
    print(f"Then open a web browser to http://[IP_ADDRESS]:5000")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000) 