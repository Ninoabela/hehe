from flask import render_template, request, current_app
from werkzeug.utils import secure_filename
from . import damage_bp
from ultralytics import YOLO
import os, time, cv2

UPLOAD_FOLDER = 'static/damage_detection/uploads'
DAMAGE_DETECTED = 'static/damage_detection/damage_detected'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DAMAGE_DETECTED, exist_ok=True)

model = YOLO("damage_detection/best.pt")  # updated path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@damage_bp.route('/detect', methods=['GET', 'POST'])
def upload_file():
    uploaded_file_urls = []
    damage_detected_urls = []

    if request.method == 'POST':
        files = request.files.getlist('media')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                uploaded_file_urls.append(f"damage_detection/uploads/{filename}")

                # Detect damage
                damage_url = detect_damage(filepath)
                damage_url = damage_url.replace("\\", "/")
                damage_detected_urls.append(damage_url)
                

    return render_template('detect.html',
                       uploaded_file_urls=uploaded_file_urls,
                       damage_detected_urls=damage_detected_urls)

def detect_damage(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    timestamp = int(time.time())

    if ext in {'png', 'jpg', 'jpeg'}:
        img = cv2.imread(file_path)
        results = model(img)[0]
        annotated = results.plot()
        output_path = os.path.join(DAMAGE_DETECTED, f"damage_{timestamp}.jpg")
        cv2.imwrite(output_path, annotated)
        return output_path

    elif ext == 'mp4':
        cap = cv2.VideoCapture(file_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

        output_path = os.path.join(DAMAGE_DETECTED, f"damage_{timestamp}.mp4")
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'X264'), fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame)[0]
            out.write(results.plot())
        cap.release()
        out.release()
        
        return output_path
