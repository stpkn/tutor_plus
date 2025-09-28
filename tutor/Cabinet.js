// Компонент личного кабинета
function Cabinet() {
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
                    <h1>Личный кабинет ученика</h1>
                    <h2>Управление обучением</h2>
                    <p className="subtitle">Отслеживайте прогресс и планируйте занятия</p>
                </div>
            </header>

            {/* Форма входа */}
            <section className="login-section">
                <h2>🔐 Вход в систему</h2>
                <div className="login-container">
                    <div className="login-form">
                        <div className="form-group">
                            <label>Email или телефон:</label>
                            <input type="text" placeholder="Введите email или телефон" />
                        </div>
                        <div className="form-group">
                            <label>Пароль:</label>
                            <input type="password" placeholder="Введите пароль" />
                        </div>
                        <button className="login-btn">Войти</button>
                        <div className="login-links">
                            <a href="#" className="forgot-password">Забыли пароль?</a>

                        </div>
                    </div>
                </div>
            </section>




        </div>
    );
}
