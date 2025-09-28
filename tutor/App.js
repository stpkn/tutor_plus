// Страница репетитора по информатике
function App() {
    return (
        <div className="container">
            {/* Навигационное меню */}
            <nav className="navbar">
                <div className="nav-brand">
                    <span>📚 Репетитор</span>
                </div>
                <ul className="nav-menu">
                    <li><a href="#about">О себе</a></li>
                    <li><a href="#education">Образование</a></li>
                    <li><a href="#courses">Курсы</a></li>
                    <li><a href="#lessons">Уроки</a></li>
                    <li><a href="#reviews">Отзывы</a></li>
                    <li><a href="#contact">Контакты</a></li>
                    <li><a href="/cabinet">Личный кабинет</a></li>
                </ul>
            </nav>

            {/* Заголовок и фото */}
            <header className="header" id="about">
                <div className="photo-section">
                    <img src="me.jpg" alt="Фото репетитора" className="photo" />
                </div>
                <div className="header-info">
                    <h1>Репетитор по информатике</h1>
                    <h2>Подготовка к ЕГЭ и ОГЭ</h2>
                    <p className="subtitle">Индивидуальные занятия • Онлайн</p>
                </div>
            </header>

            {/* Образование */}
            <section className="education" id="education">
                <h2>🎓 Образование</h2>
                <div className="education-item">
                    <h3>ГУАП (Государственный университет аэрокосмического приборостроения)</h3>
                    <p><strong>Специальность:</strong> Прикладная информатика</p>
                    <p><strong>Статус:</strong> Студент 2 курса</p>
                </div>
            </section>

            {/* О курсе */}
            <section className="course-info" id="courses">
                <h2>📚 О курсе подготовки</h2>
                <div className="course-grid">
                    <div className="course-card">
                        <h3>ЕГЭ по информатике</h3>
                        <ul>
                            <li>Программирование на Python</li>
                            <li>Алгоритмы и структуры данных</li>
                            <li>Логика и теория множеств</li>
                            <li>Системы счисления</li>
                            <li>Базы данных и SQL</li>
                        </ul>
                    </div>
                    <div className="course-card">
                        <h3>ОГЭ по информатике</h3>
                        <ul>
                            <li>Основы программирования</li>
                            <li>Алгоритмизация</li>
                            <li>Работа с текстовыми редакторами</li>
                            <li>Электронные таблицы</li>
                            <li>Компьютерные сети</li>
                        </ul>
                    </div>
                </div>
            </section>

            {/* Как проходят уроки */}
            <section className="lessons" id="lessons">
                <h2>💻 Как проходят уроки</h2>
                <div className="lessons-content">
                    <div className="lesson-step">
                        <div className="step-number">1</div>
                        <div className="step-content">
                            <h3>Диагностика знаний</h3>
                            <p>Определяем текущий уровень и пробелы в знаниях</p>
                        </div>
                    </div>
                    <div className="lesson-step">
                        <div className="step-number">2</div>
                        <div className="step-content">
                            <h3>Индивидуальный план</h3>
                            <p>Составляем персональную программу обучения</p>
                        </div>
                    </div>
                    <div className="lesson-step">
                        <div className="step-number">3</div>
                        <div className="step-content">
                            <h3>Практические занятия</h3>
                            <p>Решаем задачи, пишем программы, разбираем сложные темы</p>
                        </div>
                    </div>
                    <div className="lesson-step">
                        <div className="step-number">4</div>
                        <div className="step-content">
                            <h3>Контроль прогресса</h3>
                            <p>Регулярные проверочные работы и анализ результатов</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Отзывы */}
            <section className="reviews" id="reviews">
                <h2>⭐ Отзывы учеников</h2>
                <div className="reviews-grid">
                    <div className="review-card">
                        <div className="review-header">
                            <div className="reviewer-info">
                                <strong>Анна К.</strong>
                                <span>11 класс</span>
                            </div>
                            <div className="rating">⭐⭐⭐⭐⭐</div>
                        </div>
                        <p>"Отличный репетитор! Объясняет сложные темы простым языком. Благодаря занятиям сдала ЕГЭ на 85 баллов. Очень рекомендую!"</p>
                    </div>
                    
                    <div className="review-card">
                        <div className="review-header">
                            <div className="reviewer-info">
                                <strong>Михаил С.</strong>
                                <span>9 класс</span>
                            </div>
                            <div className="rating">⭐⭐⭐⭐⭐</div>
                        </div>
                        <p>"Подготовился к ОГЭ за 3 месяца. Репетитор помог разобраться с программированием и алгоритмами. Результат - 5!"</p>
                    </div>
                    
                    <div className="review-card">
                        <div className="review-header">
                            <div className="reviewer-info">
                                <strong>Елена В.</strong>
                                <span>10 класс</span>
                            </div>
                            <div className="rating">⭐⭐⭐⭐⭐</div>
                        </div>
                        <p>"Занятия проходят интересно и продуктивно. Много практики, мало теории. Уже вижу прогресс в решении задач!"</p>
                    </div>
                    
                    <div className="review-card">
                        <div className="review-header">
                            <div className="reviewer-info">
                                <strong>Дмитрий Р.</strong>
                                <span>11 класс</span>
                            </div>
                            <div className="rating">⭐⭐⭐⭐⭐</div>
                        </div>
                        <p>"Лучший репетитор! Индивидуальный подход, терпеливое объяснение. Сдал ЕГЭ на 92 балла и поступил в МГУ!"</p>
                    </div>
                </div>
            </section>

            {/* Контакты */}
            <section className="contact" id="contact">
                <h2>📞 Контакты</h2>
                <div className="contact-info">
                    <p><strong>Телефон:</strong> +7 (911) 270-27-28</p>
                    <p><strong>Email:</strong> stepkina.maria@outlook.com</p>
                    <p><strong>Telegram:</strong> @ms_s34</p>

                </div>
            </section>
        </div>
    );
}