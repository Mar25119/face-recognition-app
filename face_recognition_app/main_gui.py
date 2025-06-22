# main_gui.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from io import BytesIO
from webcam_core import recognize_faces, get_known_data
from face_db_manager import get_all_faces, delete_face, update_face_name


class FaceRecognitionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Распознавание лиц")

        self.known_encodings, self.known_names = get_known_data()

        # Панель с видео
        self.panel = tk.Label(window)
        self.panel.pack(padx=10, pady=10)

        # Кнопки
        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack(pady=10)

        self.add_button = tk.Button(self.btn_frame, text="Добавить лицо", command=self.add_face)
        self.add_button.pack(side="left", padx=5)

        self.view_button = tk.Button(self.btn_frame, text="Просмотреть лица", command=self.view_faces)
        self.view_button.pack(side="left", padx=5)

        self.quit_button = tk.Button(self.btn_frame, text="Выход", command=self.quit_app)
        self.quit_button.pack(side="left", padx=5)

        # Захват видео
        self.video_capture = cv2.VideoCapture(0)
        self.delay = 15
        self.current_frame = None
        self.process_this_frame = True

        self.update()

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.current_frame = frame.copy()

            if self.process_this_frame:
                locations, names = recognize_faces(frame, self.known_encodings, self.known_names)
                self.draw_boxes(frame, locations, names)

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img

        self.process_this_frame = not self.process_this_frame
        self.window.after(self.delay, self.update)

    def draw_boxes(self, frame, locations, names):
        for (top, right, bottom, left), name in zip(locations, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def add_face(self):
        if self.current_frame is not None:
            name = simpledialog.askstring("Имя", "Введите имя:")
            if name:
                from utils import add_new_face
                add_new_face(self.current_frame, name)
                self.known_encodings, self.known_names = get_known_data()

    def view_faces(self):
        ViewWindow(self.window, self)

    def quit_app(self):
        self.video_capture.release()
        self.window.destroy()


class ViewWindow:
    def __init__(self, parent, app):
        self.app = app
        self.top = tk.Toplevel(parent)
        self.top.title("Известные лица")

        self.frame = tk.Frame(self.top)
        self.frame.pack(padx=10, pady=10)

        self.rows = get_all_faces()
        self.labels = []

        for row in self.rows:
            face_id, name, photo_blob, _ = row
            img = Image.open(BytesIO(photo_blob))
            img.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(img)

            panel = tk.Label(self.frame, image=photo)
            panel.image = photo
            panel.grid(row=len(self.labels), column=0)

            entry = tk.Entry(self.frame)
            entry.insert(0, name)
            entry.grid(row=len(self.labels), column=1)

            save_btn = tk.Button(self.frame, text="Сохранить", command=lambda eid=face_id, e=entry: self.save_name(eid, e))
            save_btn.grid(row=len(self.labels), column=2)

            del_btn = tk.Button(self.frame, text="Удалить", command=lambda eid=face_id: self.delete_face(eid))
            del_btn.grid(row=len(self.labels), column=3)

            self.labels.append((panel, entry, save_btn, del_btn))

    def save_name(self, face_id, entry):
        new_name = entry.get()
        update_face_name(face_id, new_name)
        self.app.known_encodings, self.app.known_names = get_known_data()

    def delete_face(self, face_id):
        delete_face(face_id)
        self.app.known_encodings, self.app.known_names = get_known_data()
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()