# webcam_core.py

import cv2
import face_recognition
import numpy as np
from utils import load_known_data

def recognize_faces(frame, known_encodings, known_names):
    """
    Распознаёт лица на кадре.
    :param frame: текущий кадр с камеры
    :param known_encodings: список эмбеддингов известных лиц
    :param known_names: список имён известных лиц
    :return: координаты лиц и соответствующие имена
    """
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    face_names = []
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        face_names.append(name)

    scaled_locations = [(t * 4, r * 4, b * 4, l * 4) for (t, r, b, l) in face_locations]
    return scaled_locations, face_names


def get_known_data():
    """
    Загружает данные о известных лицах из БД.
    :return: список эмбеддингов и имён
    """
    return load_known_data()
