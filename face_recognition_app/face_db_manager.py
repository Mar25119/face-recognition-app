# face_db_manager.py

import sqlite3

class FaceDBManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_db()

    def _connect(self):
        """Внутренний метод: создаёт соединение с БД"""
        return sqlite3.connect(self.db_path)

    def _execute_query(self, query, params=(), fetch=False):
        """
        Универсальный метод для выполнения SQL-запросов
        :param query: SQL-запрос
        :param params: параметры запроса
        :param fetch: нужно ли вернуть результат (для SELECT)
        :return: результат запроса (если fetch=True), иначе None
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()

    def init_db(self):
        """Создаёт таблицу faces, если её нет"""
        query = """
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                photo BLOB NOT NULL,
                encoding BLOB NOT NULL
            )
        """
        self._execute_query(query)

    def add_face(self, name, photo_blob, encoding_blob):
        """Добавляет новое лицо в БД"""
        query = "INSERT INTO faces (name, photo, encoding) VALUES (?, ?, ?)"
        self._execute_query(query, (name, photo_blob, encoding_blob))

    def get_all_faces(self):
        """Возвращает все записи из таблицы faces"""
        query = "SELECT id, name, photo, encoding FROM faces"
        return self._execute_query(query, fetch=True)

    def delete_face(self, face_id):
        """Удаляет запись по ID"""
        query = "DELETE FROM faces WHERE id = ?"
        self._execute_query(query, (face_id,))

    def update_face_name(self, face_id, new_name):
        """Обновляет имя лица по ID"""
        query = "UPDATE faces SET name = ? WHERE id = ?"
        self._execute_query(query, (new_name, face_id))
