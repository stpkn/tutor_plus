function Cabinet() {
    console.log('🔧 Cabinet компонент создан');

    // Состояние для формы входа
    const [loginData, setLoginData] = React.useState({
        username: '',
        password: ''
    });
    const [isLoading, setIsLoading] = React.useState(false);

    console.log('🔄 Инициализировано состояние:', loginData);

    // Обработчик изменения полей ввода
    const handleInputChange = (field, value) => {
        console.log('📝 Изменение поля:', field, value);
        setLoginData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    // Обработчик отправки формы
    const handleLogin = async (e) => {
        e.preventDefault();

        console.log('🔄 Начало обработки входа', loginData);

        if (!loginData.username || !loginData.password) {
            console.log('❌ Пустые поля');
            alert('Пожалуйста, заполните все поля');
            return;
        }

        setIsLoading(true);
        console.log('⏳ Установлен isLoading:', true);

        try {
            console.log('📨 Отправка запроса на /api/login...');
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: loginData.username,
                    password: loginData.password
                })
            });

            console.log('✅ Ответ получен, статус:', response.status);
            const data = await response.json();
            console.log('📊 Данные ответа:', data);

            if (data.success) {
                console.log('✅ Успешный вход, редирект на:', data.redirect_url);
                alert('✅ ' + data.message);
                // Редирект на соответствующий кабинет
                window.location.href = data.redirect_url;
            } else {
                console.log('❌ Ошибка входа:', data.message);
                alert('❌ ' + data.message);
            }
        } catch (error) {
            console.error('❌ Ошибка fetch:', error);
            alert('⚠️ Ошибка при входе в систему');
        } finally {
            setIsLoading(false);
            console.log('⏳ Установлен isLoading:', false);
        }
    };

    // Обработчик нажатия Enter
    const handleKeyPress = (e) => {
        console.log('⌨️ Нажата клавиша:', e.key);
        if (e.key === 'Enter') {
            handleLogin(e);
        }
    };

    console.log('🎨 Рендеринг компонента...');

    return (
        <div className="container">
            {/* Навигационное меню */}
            <nav className="navbar">
                <div className="nav-brand">
                    <span>👤 Личный кабинет</span>
                </div>
                <ul className="nav-menu">
                    <li><a href="/">Главная</a></li>
                    <li><a href="#login">Вход</a></li>
                </ul>
            </nav>

            {/* Заголовок */}
            <header className="header" id="login">
                <div className="header-info">
                    <h1>Личный кабинет</h1>
                    <h2>Управление обучением</h2>
                    <p className="subtitle">Отслеживайте прогресс и планируйте занятия</p>

                    {/* Блок с тестовыми данными */}
                    <div className="test-accounts">
                        <h3>Тестовые аккаунты:</h3>
                        <div className="account-list">
                            <div className="account-item">
                                <strong>Репетитор:</strong> логин <code>tutor</code>, пароль <code>tutor</code>
                            </div>
                            <div className="account-item">
                                <strong>Ученик:</strong> создается репетитором
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Форма входа */}
            <section className="login-section">
                <h2>🔐 Вход в систему</h2>
                <div className="login-container">
                    <form className="login-form" onSubmit={handleLogin}>
                        <div className="form-group">
                            <label>Логин:</label>
                            <input
                                type="text"
                                placeholder="Введите логин"
                                value={loginData.username}
                                onChange={(e) => handleInputChange('username', e.target.value)}
                                onKeyPress={handleKeyPress}
                                disabled={isLoading}
                            />
                        </div>
                        <div className="form-group">
                            <label>Пароль:</label>
                            <input
                                type="password"
                                placeholder="Введите пароль"
                                value={loginData.password}
                                onChange={(e) => handleInputChange('password', e.target.value)}
                                onKeyPress={handleKeyPress}
                                disabled={isLoading}
                            />
                        </div>
                        <button
                            type="submit"
                            className="login-btn"
                            disabled={isLoading}
                        >
                            {isLoading ? '⏳ Вход...' : '🔐 Войти'}
                        </button>
                        <div className="login-links">
                            <a href="#" className="forgot-password">Забыли пароль?</a>
                        </div>
                    </form>
                </div>
            </section>
        </div>
    );
}

console.log('📁 Cabinet.js загружен');