from database.database import Database
from models.user import User


class AuthService:
    def __init__(self, db: Database):
        self.db = db
        self.current_user = None

    def login(self, username: str, password: str):
        """Аутентификация пользователя"""
        print(f"🔐 AuthService: получен запрос для пользователя '{username}'")
        user_data = self.db.authenticate_user(username, password)

        if user_data:
            user = User(**user_data)
            self.current_user = user
            role_name = "репетитор" if user.role == 'tutor' else "ученик"
            print(f"✅ AuthService: успешный вход для {role_name} {user.first_name}")
            return True, f"Успешный вход! Вы вошли как {role_name}", user
        else:
            print(f"❌ AuthService: аутентификация не удалась для '{username}'")
            return False, "Неверный логин или пароль", User()

    def logout(self):
        """Выход из системы"""
        self.current_user = None