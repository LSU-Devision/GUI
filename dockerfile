# Use Python 3.10 (since TensorFlow 2.10 does not support 3.11)
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (for Tkinter and TensorFlow)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the display variable (for GUI on Linux/macOS)
ENV DISPLAY=:0

# Run the Tkinter application when the container starts
CMD ["python", "src/pages.py"]
