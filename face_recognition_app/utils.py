# utils.py
import numpy as np
import face_recognition
import cv2
from io import BytesIO
from PIL import Image
from face_db_manager import get_all_faces


def load_known_data():
    """Загружает из БД эмбеддинги и имена."""
    encodings = []
    names = []
    rows = get_all_faces()
    for row in rows:
        _, name, _, encoding_blob = row
        encoding = np.frombuffer(encoding_blob, dtype=np.float64)
        encodings.append(encoding)
        names.append(name)
    return encodings, names


def add_new_face(frame, name):
    """Добавляет новое лицо из кадра в БД."""
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')
    photo_blob = img_byte_arr.getvalue()

    # Получаем эмбеддинг
    encoding = face_recognition.face_encodings(image)
    if len(encoding) == 0:
        print("Не найдено лицо на кадре.")
        return
    encoding_blob = encoding[0].tobytes()

    from face_db_manager import add_face
    add_face(name, photo_blob, encoding_blob)