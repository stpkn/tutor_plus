from database.database import Database

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.role = kwargs.get('role')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.lesson_price = kwargs.get('lesson_price')
        self.contact_info = kwargs.get('contact_info')
        self.is_active = kwargs.get('is_active')
        self.created_by = kwargs.get('created_by')
        self.created_at = kwargs.get('created_at')
        self.exam_type = kwargs.get('exam_type')  # Может быть None для репетитора

    def verify_password(self, password):
        return self.password_hash == password


class AuthService:
    def __init__(self, db: Database):
        self.db = db
        self.current_user = None

    def login(self, username, password):
        try:
            user_data = self.db.authenticate_user(username, password)

            if user_data:
                # Убедимся, что все необходимые поля есть
                required_fields = ['id', 'username', 'password_hash', 'role', 'first_name', 'last_name']
                for field in required_fields:
                    if field not in user_data:
                        print(f"❌ Отсутствует обязательное поле: {field}")
                        return False, f"Отсутствует поле {field} в данных пользователя", None

                user = User(**user_data)
                if user.verify_password(password):
                    self.current_user = user
                    print(f"✅ Успешный вход: {user.role} {user.first_name}")
                    return True, "Успешный вход", user
                else:
                    print("❌ Неверный пароль")
                    return False, "Неверный пароль", None
            else:
                print("❌ Пользователь не найден")
                return False, "Пользователь не найден", None

        except Exception as e:
            print(f"❌ Ошибка при входе: {e}")
            return False, f"Ошибка при входе: {str(e)}", None

    def logout(self):
        self.current_user = None
        return True, "Успешный выход"

    def get_current_user(self):
        return self.current_user

    def is_authenticated(self):
        return self.current_user is not None