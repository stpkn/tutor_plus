import sqlite3
import os
from typing import Optional, Dict, Any


class Database:
    def __init__(self, db_path='database/tutoring.db'):
        self.db_path = db_path
    def get_connection(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            print(f"❌ Ошибка подключения: {e}")
            return None

    def connect(self):
        return self.get_connection()

    def create_tables(self):
        """Создание таблиц из SQL скрипта"""
        connection = self.get_connection()
        if not connection:
            return

        try:
            if not os.path.exists('database/schema.sql'):
                print("❌ Файл database/schema.sql не найден!")
                return

            print("📁 Чтение database/schema.sql...")
            with open('database/schema.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
                print(f"📄 Размер скрипта: {len(sql_script)} символов")

            cursor = connection.cursor()
            cursor.executescript(sql_script)
            connection.commit()
            print("✅ Таблицы созданы")

            # Проверка, создался ли пользователь tutor
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'tutor'")
            result = cursor.fetchone()
            print(f"👤 Пользователей 'tutor' в базе: {result['count']}")

        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")
        finally:
            connection.close()

    def authenticate_user(self, username: str, password: str):
        """Аутентификация пользователя"""
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if not user:
                print(f"❌ Пользователь '{username}' не найден")
                return None

            user_dict = dict(user)
            print(f"✅ Пользователь найден: {user_dict}")
            print(f"🔑 Сравнение паролей: введен '{password}', в базе '{user_dict['password_hash']}'")

            # Простое сравнение паролей
            if user_dict['password_hash'] == password:
                print("✅ Пароль верный!")
                return user_dict
            else:
                print("❌ Неверный пароль")
                return None

        except sqlite3.Error as e:
            print(f"❌ Ошибка аутентификации: {e}")
            return None
        finally:
            connection.close()

    def create_student(self, username: str, password: str, first_name: str,
                       last_name: str, tutor_id: int, contact_info: str = "") -> bool:
        """Создание нового ученика"""
        connection = self.get_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, created_by, contact_info)
                VALUES (?, ?, 'student', ?, ?, ?, ?)
            """, (username, password, first_name, last_name, tutor_id, contact_info))

            connection.commit()
            return cursor.lastrowid is not None
        except sqlite3.Error as e:
            print(f"❌ Ошибка создания ученика: {e}")
            return False
        finally:
            connection.close()

    def get_tutor_students(self, tutor_id: int):
        """Получение всех учеников репетитора"""
        connection = self.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, username, first_name, last_name, contact_info, created_at
                FROM users 
                WHERE created_by = ? AND role = 'student' AND is_active = 1
                ORDER BY created_at DESC
            """, (tutor_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения учеников: {e}")
            return []
        finally:
            connection.close()

    def get_student_schedule(self, student_id: int):
        """Получение расписания ученика"""
        connection = self.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT s.id, s.day_of_week, s.start_time, s.end_time, s.lesson_link, s.status,
                       t.title as topic_title, u.first_name as tutor_name
                FROM schedule s
                JOIN topics t ON s.topic_id = t.id
                JOIN users u ON s.tutor_id = u.id
                WHERE s.student_id = ? AND s.status = 'active'
                ORDER BY 
                    CASE s.day_of_week
                        WHEN 'monday' THEN 1
                        WHEN 'tuesday' THEN 2
                        WHEN 'wednesday' THEN 3
                        WHEN 'thursday' THEN 4
                        WHEN 'friday' THEN 5
                        WHEN 'saturday' THEN 6
                        WHEN 'sunday' THEN 7
                    END,
                    s.start_time
            """, (student_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения расписания: {e}")
            return []
        finally:
            connection.close()

    def get_tutor_schedule(self, tutor_id: int):
        """Получение расписания репетитора"""
        connection = self.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT s.id, s.day_of_week, s.start_time, s.end_time, s.lesson_link, s.status,
                       t.title as topic_title, 
                       u.first_name as student_name, u.last_name as student_last_name
                FROM schedule s
                JOIN topics t ON s.topic_id = t.id
                JOIN users u ON s.student_id = u.id
                WHERE s.tutor_id = ? AND s.status = 'active'
                ORDER BY 
                    CASE s.day_of_week
                        WHEN 'monday' THEN 1
                        WHEN 'tuesday' THEN 2
                        WHEN 'wednesday' THEN 3
                        WHEN 'thursday' THEN 4
                        WHEN 'friday' THEN 5
                        WHEN 'saturday' THEN 6
                        WHEN 'sunday' THEN 7
                    END,
                    s.start_time
            """, (tutor_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения расписания репетитора: {e}")
            return []
        finally:
            connection.close()