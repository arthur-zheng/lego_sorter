import os
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory

# Set the directory to save images
IMAGE_DIR = os.path.join(app.root_path, 'static', 'images', 'captures')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    part_number_1 = request.form['part_number1']
    part_number_2 = request.form['part_number2']
    part_number = f"{part_number_1} {part_number_2}"

    color = request.form['color']

    # Capture image from first camera
    timestamp1 = datetime.now().strftime('%Y%m%d%H%M%S')
    filename1 = f"{part_number}_{color}_{timestamp1}_cam1.jpg"
    filepath1 = os.path.join(IMAGE_DIR, filename1)
    command1 = f"libcamera-still -o {filepath1} --nopreview -n --camera 0"
    subprocess.run(command1, shell=True)

    # Capture image from second camera after a short delay for a different timestamp
    timestamp2 = datetime.now().strftime('%Y%m%d%H%M%S')
    filename2 = f"{part_number}_{color}_{timestamp2}_cam2.jpg"
    filepath2 = os.path.join(IMAGE_DIR, filename2)
    command2 = f"libcamera-still -o {filepath2} --nopreview -n --camera 1"
    subprocess.run(command2, shell=True)

    # Save label information to CSV file for both images
    with open('data.csv', 'a') as f:
        f.write(f"{filename1},{part_number},{color},cam1\n")
        f.write(f"{filename2},{part_number},{color},cam2\n")

    return render_template('success.html', filename1=filename1, filename2=filename2)

@app.route('/images/<filename>')
def display_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)