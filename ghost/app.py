import os
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_folder='static')

# Set the directory to save images
IMAGE_DIR = os.path.join(app.root_path, 'static', 'images', 'captures')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

WIDTH_OF_IMAGE = 1200
HEIGHT_OF_IMAGE = 800
EV_CAM_0 = 0.4
EV_CAM_1 = 0.4

CROP_IMAGE = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    element_id = request.form['element_id']
    design_id = request.form['design_id']
    part_number = f"{element_id}_{design_id}"

    color = request.form['color']

    width_height_ev = f"--width {WIDTH_OF_IMAGE} --height {HEIGHT_OF_IMAGE} --ev {EV_CAM_0}" if CROP_IMAGE == True else ""

    # Capture image from first camera
    timestamp1 = datetime.now().strftime('%Y%m%d%H%M%S')
    filename1 = f"{part_number}_{color}_{timestamp1}_cam1.jpg"
    filepath1 = os.path.join(IMAGE_DIR, filename1)
    command1 = f"libcamera-still -o {filepath1} {width_height_ev} --nopreview -n --camera 0"
    subprocess.run(command1, shell=True)

    # Capture image from second camera after a short delay for a different timestamp
    timestamp2 = datetime.now().strftime('%Y%m%d%H%M%S')
    filename2 = f"{part_number}_{color}_{timestamp2}_cam1.jpg"
    filepath2 = os.path.join(IMAGE_DIR, filename2)
    command2 = f"libcamera-still -o {filepath2} {width_height_ev} --nopreview -n --camera 1"
    subprocess.run(command2, shell=True)

    # Save label information to CSV file for both images
    with open('data.csv', 'a') as f:
        f.write(f"{filename1},{element_id},{design_id},{color},cam1\n")
        f.write(f"{filename2},{element_id},{design_id},{color},cam2\n")

    return render_template('success.html', filename1=filename1, filename2=filename2)

@app.route('/images/<filename>')
def display_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)