from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, session
import os
from database.database import Database
from services.auth_service import AuthService

# Инициализация БД
db = Database('database/tutoring.db')
auth_service = AuthService(db)

# Создаем таблицы при запуске
db.create_tables()

app = Flask(__name__)
app.secret_key = 'tutoring-secret-key-2024'

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint для входа в систему"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"🔐 Попытка входа: username='{username}', password='{password}'")
    print(f"🔐 Типы данных: username={type(username)}, password={type(password)}")

    success, message, user = auth_service.login(username, password)

    if success:
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name

        print(f"✅ Успешный вход: {user.role} {user.first_name} (ID: {user.id})")
        return jsonify({
            'success': True,
            'message': message,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'lesson_price': user.lesson_price,
                'contact_info': user.contact_info
            },
            'redirect_url': '/tutor-cabinet' if user.role == 'tutor' else '/student-cabinet'
        })
    else:
        print(f"❌ Ошибка входа: {message}")
        return jsonify({
            'success': False,
            'message': message
        }), 401


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API endpoint для выхода из системы"""
    session.clear()
    auth_service.logout()
    return jsonify({
        'success': True,
        'message': 'Вы успешно вышли из системы'
    })


@app.route('/api/check-auth')
def check_auth():
    """Проверка статуса аутентификации"""
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'role': session['role'],
                'first_name': session['first_name'],
                'last_name': session['last_name']
            }
        })
    else:
        return jsonify({'authenticated': False})


@app.route('/api/tutor/students', methods=['GET'])
def get_tutor_students():
    """Получение списка учеников для репетитора"""
    if 'user_id' not in session or session['role'] != 'tutor':
        return jsonify({'error': 'Доступ запрещен'}), 403

    students = db.get_tutor_students(session['user_id'])
    return jsonify({'students': students})


@app.route('/api/tutor/create-student', methods=['POST'])
def create_student():
    """Создание нового ученика"""
    if 'user_id' not in session or session['role'] != 'tutor':
        return jsonify({'error': 'Доступ запрещен'}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_info = data.get('contact_info', '')

    if not all([username, password, first_name, last_name]):
        return jsonify({'success': False, 'message': 'Все поля обязательны'}), 400

    success = db.create_student(username, password, first_name, last_name, session['user_id'], contact_info)

    if success:
        return jsonify({'success': True, 'message': 'Ученик успешно создан'})
    else:
        return jsonify({'success': False, 'message': 'Ошибка при создании ученика'}), 500


@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """Получение расписания для текущего пользователя"""
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизован'}), 401

    user_id = session['user_id']
    role = session['role']

    if role == 'tutor':
        schedule = db.get_tutor_schedule(user_id)
    else:
        schedule = db.get_student_schedule(user_id)

    return jsonify({'schedule': schedule})


@app.route('/api/tutor/schedule', methods=['POST'])
def create_schedule():
    """Создание расписания (только для репетитора)"""
    if 'user_id' not in session or session['role'] != 'tutor':
        return jsonify({'error': 'Доступ запрещен'}), 403

    data = request.get_json()
    student_id = data.get('student_id')
    topic_id = data.get('topic_id')
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    lesson_link = data.get('lesson_link', '')

    return jsonify({'success': True, 'message': 'Расписание создано'})


# Отладочные Routes
@app.route('/debug/templates')
def debug_templates():
    """Проверка доступности template файлов"""
    import os

    files_to_check = [
        'templates/cabinet.html',
        'templates/tutor_cabinet.html',
        'templates/student_cabinet.html'
    ]

    result = {}
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        result[file_path] = {
            'exists': exists,
            'absolute_path': os.path.abspath(file_path) if exists else None,
            'readable': os.access(file_path, os.R_OK) if exists else False
        }

        if exists:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    result[file_path]['size'] = len(content)
                    result[file_path]['first_100_chars'] = content[:100]
            except Exception as e:
                result[file_path]['error'] = str(e)

    return jsonify(result)


@app.route('/debug/files')
def debug_files():
    """Отладочная страница для проверки файлов"""
    import os
    result = {
        'current_directory': os.getcwd(),
        'app_file_path': os.path.abspath(__file__),
        'templates_path': os.path.abspath('templates'),
        'templates_exists': os.path.exists('templates'),
    }

    if os.path.exists('templates'):
        result['files_in_templates'] = os.listdir('templates')
        # Проверим конкретные файлы
        result['cabinet_exists'] = os.path.exists('templates/cabinet.html')
        result['tutor_cabinet_exists'] = os.path.exists('templates/tutor_cabinet.html')
        result['student_cabinet_exists'] = os.path.exists('templates/student_cabinet.html')

    return jsonify(result)


@app.route('/debug/db')
def debug_db():
    """Отладочная страница для проверки базы данных"""
    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        # Проверка таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Проверка пользователей
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        connection.close()

        result = {
            'tables': [dict(table) for table in tables],
            'users': [dict(user) for user in users],
            'total_users': len(users)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tutor-cabinet')
def tutor_cabinet():
    if 'user_id' not in session or session['role'] != 'tutor':
        return "Доступ запрещен. Только для репетиторов.", 403

    try:
        with open('templates/tutor_cabinet.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Если файл не найден, создаем простую страницу
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Кабинет репетитора</title>
            <link rel="stylesheet" href="/styles.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <div class="nav-brand"><span>🎓 Кабинет репетитора</span></div>
                    <ul class="nav-menu">
                        <li><a href="/">Главная</a></li>
                        <li><a href="/cabinet">Выйти</a></li>
                    </ul>
                </nav>
                <header class="header">
                    <div class="header-info">
                        <h1>Добро пожаловать, репетитор!</h1>
                        <h2>Вы успешно вошли в систему</h2>
                        <p>ID: {session.get('user_id')}, Имя: {session.get('first_name')} {session.get('last_name')}</p>
                    </div>
                </header>
                <section class="login-section">
                    <h2>🎉 Поздравляем! Система аутентификации работает!</h2>
                    <div class="login-container">
                        <p><strong>Репетитор:</strong> {session.get('first_name')} {session.get('last_name')}</p>
                        <p><strong>Логин:</strong> {session.get('username')}</p>
                        <p><strong>ID:</strong> {session.get('user_id')}</p>
                        <p>Основной кабинет будет доступен после настройки шаблонов.</p>
                        <button onclick="logout()" class="login-btn">Выйти</button>
                    </div>
                </section>
            </div>
            <script>
                function logout() {{
                    fetch('/api/logout', {{method: 'POST'}}).then(() => window.location.href = '/cabinet');
                }}
            </script>
        </body>
        </html>
        """

@app.route('/student-cabinet')
def student_cabinet():
    """Кабинет ученика"""
    if 'user_id' not in session or session['role'] != 'student':
        return "Доступ запрещен. Только для учеников.", 403

    try:
        with open('templates/student_cabinet.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Если файл не найден, создаем простую страницу
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Кабинет ученика</title>
            <link rel="stylesheet" href="/styles.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <div class="nav-brand"><span>📚 Кабинет ученика</span></div>
                    <ul class="nav-menu">
                        <li><a href="/">Главная</a></li>
                        <li><a href="/cabinet">Выйти</a></li>
                    </ul>
                </nav>
                <header class="header">
                    <div class="header-info">
                        <h1>Добро пожаловать, ученик!</h1>
                        <h2>Вы успешно вошли в систему</h2>
                        <p>ID: {session.get('user_id')}, Имя: {session.get('first_name')} {session.get('last_name')}</p>
                    </div>
                </header>
                <section class="login-section">
                    <h2>🎉 Поздравляем! Система аутентификации работает!</h2>
                    <div class="login-container">
                        <p><strong>Ученик:</strong> {session.get('first_name')} {session.get('last_name')}</p>
                        <p><strong>Логин:</strong> {session.get('username')}</p>
                        <p><strong>ID:</strong> {session.get('user_id')}</p>
                        <p>Основной кабинет будет доступен после настройки шаблонов.</p>
                        <button onclick="logout()" class="login-btn">Выйти</button>
                    </div>
                </section>
            </div>
            <script>
                function logout() {{
                    fetch('/api/logout', {{method: 'POST'}}).then(() => window.location.href = '/cabinet');
                }}
            </script>
        </body>
        </html>
        """

@app.route('/')
def index():
    """Главная страница с React приложением"""
    return render_template('index.html')

@app.route('/cabinet')
def cabinet():
    """Страница личного кабинета"""
    return render_template('cabinet.html')

@app.route('/App.js')
def serve_app_js():
    """Обслуживание App.js"""
    return send_file('App.js', mimetype='application/javascript')

@app.route('/index.js')
def serve_index_js():
    """Обслуживание index.js"""
    return send_file('index.js', mimetype='application/javascript')

@app.route('/styles.css')
def serve_css():
    """Обслуживание styles.css"""
    return send_file('styles.css', mimetype='text/css')

@app.route('/me.jpg')
def serve_photo():
    """Обслуживание фото"""
    return send_file('me.jpg', mimetype='image/jpeg')

@app.route('/Cabinet.js')
def serve_cabinet_js():
    """Обслуживание Cabinet.js"""
    return send_file('Cabinet.js', mimetype='application/javascript')

@app.route('/cabinet-index.js')
def serve_cabinet_index_js():
    """Обслуживание cabinet-index.js"""
    return send_file('cabinet-index.js', mimetype='application/javascript')

if __name__ == '__main__':
    print("🚀 Flask сервер запущен!")
    print("📱 Откройте: http://localhost:5000")
    print("🎯 Тестовые данные:")
    print("   Репетитор: логин 'tutor', пароль 'tutor'")
    app.run(debug=True, host='0.0.0.0', port=5000)