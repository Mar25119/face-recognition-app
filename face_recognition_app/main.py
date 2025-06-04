# main.py
import cv2
import face_recognition
import numpy as np

# Загрузка обученной модели
data = np.load('encodings.npy', allow_pickle=True)
known_encodings = data['encodings']
known_names = data['names']

# Захват видео с камеры
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Конвертируем BGR (OpenCV) в RGB (face_recognition)
    rgb_frame = frame[:, :, ::-1]

    # Поиск лиц на кадре
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Неизвестный"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

        # Рисуем прямоугольник и подпись
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Отображение кадра
    cv2.imshow('Face Recognition', frame)

    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Очистка
video_capture.release()
cv2.destroyAllWindows()