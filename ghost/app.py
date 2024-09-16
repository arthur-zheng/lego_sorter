import os
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
# from picamera import PiCamera  # 如果您使用的是 libcamera，请忽略这行

app = Flask(__name__)
# camera = PiCamera()  # 如果您使用的是 libcamera，请忽略这行

# Set the directory to save images
IMAGE_DIR = os.path.join(app.root_path, 'static', 'images')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    part_number = request.form['part_number']
    color = request.form['color']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{part_number}_{color}_{timestamp}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)

    # Capture image using libcamera
    command = f"libcamera-still -o {filepath} --nopreview -n"
    subprocess.run(command, shell=True)

    # Save label information to CSV file
    with open('data.csv', 'a') as f:
        f.write(f"{filename},{part_number},{color}\n")

    return render_template('success.html', filename=filename)

@app.route('/images/<filename>')
def display_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)