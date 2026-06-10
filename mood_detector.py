import cv2
import numpy as np
import librosa

# 🧠 Facial Expression Based Detection (Simple rules)
def detect_mood_from_image(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

        if len(smiles) > 0:
            return "happy"
        else:
            return "neutral"

    return "sad"  # if no face detected, assume sad

# 🎙️ Audio-Based Mood Detection (Energy based)
def detect_mood_from_audio(audio_path):
    y, sr = librosa.load(audio_path)
    energy = np.sum(y ** 2) / len(y)

    if energy > 0.02:
        return "happy"
    elif energy > 0.005:
        return "neutral"
    else:
        return "sad"
