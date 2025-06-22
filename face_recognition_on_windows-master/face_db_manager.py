# face_db_manager.py
import sqlite3

def init_db():
    """Создаёт таблицу для хранения лиц."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            photo BLOB NOT NULL,
            encoding BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_face(name, photo_blob, encoding_blob):
    """Добавляет новое лицо в БД."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO faces (name, photo, encoding) VALUES (?, ?, ?)
    """, (name, photo_blob, encoding_blob))
    conn.commit()
    conn.close()


def get_all_faces():
    """Возвращает всех лиц из БД."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, photo, encoding FROM faces")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_face(face_id):
    """Удаляет лицо по ID."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faces WHERE id=?", (face_id,))
    conn.commit()
    conn.close()


def update_face_name(face_id, new_name):
    """Обновляет имя лица по ID."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE faces SET name=? WHERE id=?", (new_name, face_id))
    conn.commit()
    conn.close()