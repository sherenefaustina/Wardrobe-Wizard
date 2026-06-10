import cv2
from flask import Blueprint, Response, render_template, request, send_file
import numpy as np
import os
from datetime import datetime

virtual_tryon = Blueprint('virtual_tryon', __name__)

# Load Haar cascade
face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Load multiple outfit overlay images
overlay_folder = os.path.join('static', 'images', 'outfits')  # Put multiple PNGs here
overlay_images = []
for file in sorted(os.listdir(overlay_folder)):
    if file.endswith('.png'):
        img = cv2.imread(os.path.join(overlay_folder, file), cv2.IMREAD_UNCHANGED)
        if img is not None and img.shape[2] == 4:
            overlay_images.append(img)

# Track current outfit
current_overlay_index = 0

# Capture screenshot frame
latest_frame = None

def overlay_clothes(frame, overlay, face_coords):
    x, y, w, h = face_coords
    shirt_width = int(w * 2.0)
    shirt_height = int(h * 1.5)

    shirt_x1 = x - int(w * 0.5)
    shirt_y1 = y + h + 10
    shirt_x2 = shirt_x1 + shirt_width
    shirt_y2 = shirt_y1 + shirt_height

    if shirt_x1 < 0 or shirt_y1 < 0 or shirt_x2 > frame.shape[1] or shirt_y2 > frame.shape[0]:
        return frame

    overlay_resized = cv2.resize(overlay, (shirt_width, shirt_height))
    alpha_overlay = overlay_resized[:, :, 3] / 255.0

    for c in range(3):
        frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2, c] = (
            alpha_overlay * overlay_resized[:, :, c] +
            (1 - alpha_overlay) * frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2, c]
        )

    return frame


def gen_frames():
    global latest_frame, current_overlay_index
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        face_found = False

        for (x, y, w, h) in faces:
            face_found = True

            # Expand region to cover face + upper body
            shirt_x1 = x - int(w * 0.5)
            shirt_y1 = y - 30
            shirt_x2 = x + w + int(w * 0.5)
            shirt_y2 = y + h + int(h * 1.5)

            shirt_x1 = max(0, shirt_x1)
            shirt_y1 = max(0, shirt_y1)
            shirt_x2 = min(frame.shape[1], shirt_x2)
            shirt_y2 = min(frame.shape[0], shirt_y2)

            mask[shirt_y1:shirt_y2, shirt_x1:shirt_x2] = 255

            # Apply overlay
            if overlay_images:
                overlay_img = overlay_images[current_overlay_index]
                frame = overlay_clothes(frame, overlay_img, (x, y, w, h))
            break

        blurred = cv2.GaussianBlur(frame, (45, 45), 0)
        result = np.where(mask[:, :, None] == 255, frame, blurred)

        latest_frame = result.copy()  # Save latest frame for screenshot

        _, buffer = cv2.imencode('.jpg', result)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@virtual_tryon.route('/tryon')
def tryon():
    return render_template('tryon.html')


@virtual_tryon.route('/virtual_tryon_feed')
def virtual_tryon_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@virtual_tryon.route('/switch_outfit', methods=['POST'])
def switch_outfit():
    global current_overlay_index
    current_overlay_index = (current_overlay_index + 1) % len(overlay_images)
    return '', 204


@virtual_tryon.route('/capture_image', methods=['GET'])
def capture_image():
    global latest_frame
    if latest_frame is not None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join('static', 'captures', f'capture_{timestamp}.jpg')
        cv2.imwrite(path, latest_frame)
        return send_file(path, mimetype='image/jpeg', as_attachment=True)
    else:
        return 'No image to save', 400
