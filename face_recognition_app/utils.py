# utils.py
import face_recognition
import os
import numpy as np

def train_model(known_faces_dir='known_faces', output_file='encodings.npy'):
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                known_encodings.append(encoding[0])
                known_names.append(os.path.splitext(filename)[0])

    np.savez(output_file, encodings=known_encodings, names=known_names)
    print("Модель обучена и сохранена.")