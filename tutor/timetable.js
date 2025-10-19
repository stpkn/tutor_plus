// schedule.js

// Навигация между страницами
function showPage(pageId) {
    document.querySelectorAll('.page-section').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');

    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Управление представлениями расписания
function changeView(viewType) {
    // Скрыть все представления
    document.querySelectorAll('.schedule-view').forEach(view => {
        view.classList.remove('active');
    });

    // Убрать активный класс у всех кнопок
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Показать выбранное представление
    document.getElementById(viewType + 'View').classList.add('active');

    // Добавить активный класс к нажатой кнопке
    event.target.classList.add('active');

    // Обновить заголовок периода
    updatePeriodTitle(viewType);
}

// Навигация по датам
let currentDate = new Date();

function previousPeriod() {
    currentDate.setDate(currentDate.getDate() - 1);
    updatePeriodTitle(getCurrentView());
}

function nextPeriod() {
    currentDate.setDate(currentDate.getDate() + 1);
    updatePeriodTitle(getCurrentView());
}

// Получить текущее активное представление
function getCurrentView() {
    const activeView = document.querySelector('.schedule-view.active');
    if (activeView) {
        return activeView.id.replace('View', '');
    }
    return 'day';
}

// Обновить заголовок периода
function updatePeriodTitle(viewType) {
    const periodElement = document.getElementById('currentPeriod');
    const options = {
        day: 'numeric',
        month: 'long'
    };

    switch(viewType) {
        case 'day':
            periodElement.textContent = currentDate.toLocaleDateString('ru-RU', options);
            break;
        case 'week':
            const weekStart = new Date(currentDate);
            weekStart.setDate(currentDate.getDate() - currentDate.getDay() + 1);
            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekStart.getDate() + 6);

            const weekStartStr = weekStart.toLocaleDateString('ru-RU', { day: 'numeric', month: 'numeric' });
            const weekEndStr = weekEnd.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
            periodElement.textContent = `Неделя ${weekStartStr}-${weekEndStr}`;
            break;
        case 'month':
            const monthName = currentDate.toLocaleDateString('ru-RU', { month: 'long' });
            const year = currentDate.getFullYear();
            periodElement.textContent = `${monthName} ${year}`;
            break;
    }
}

// Функции для занятий
function startLesson(lessonId, studentName) {
    if (confirm(`Начать урок с учеником ${studentName}?`)) {
        alert(`Урок #${lessonId} начат с ${studentName}`);
        // Здесь будет логика начала урока
    }
}

function startAllLessons() {
    if (confirm('Начать уроки со всеми учениками?')) {
        alert('Все уроки начаты!');
        // Логика начала всех уроков
    }
}

function scheduleAllLessons() {
    if (confirm('Запланировать занятия для всех учеников?')) {
        alert('Все занятия запланированы!');
        // Логика планирования занятий
    }
}

function editLesson(lessonId) {
    alert(`Редактирование урока #${lessonId}`);
    // Логика редактирования урока
}

function showCreateLessonForm() {
    document.getElementById('createLessonModal').style.display = 'block';
}

function closeCreateLessonForm() {
    document.getElementById('createLessonModal').style.display = 'none';
}

function showWeekView() {
    changeView('week');
}

function showRecurringForm() {
    alert('Настройка повторяющихся занятий');
    // Логика настройки повторяющихся занятий
}

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Обработка формы создания занятия
    const createLessonForm = document.querySelector('.create-lesson-form');
    if (createLessonForm) {
        createLessonForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const student = formData.get('student');
            const subject = formData.get('subject');
            const topic = formData.get('topic');
            const datetime = formData.get('datetime');

            alert(`Занятие создано!\nУченик: ${student}\nПредмет: ${subject}\nТема: ${topic}\nВремя: ${datetime}`);
            closeCreateLessonForm();
            this.reset();
        });
    }

    // Закрытие модального окна при клике вне его
    window.addEventListener('click', function(e) {
        const modal = document.getElementById('createLessonModal');
        if (e.target === modal) {
            closeCreateLessonForm();
        }
    });

    // Закрытие модального окна по ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeCreateLessonForm();
        }
    });

    // Инициализация текущей даты
    updatePeriodTitle('day');

    // Проверка авторизации (если нужно)
    fetch('/api/check-auth')
        .then(response => response.json())
        .then(data => {
            if (!data.authenticated) {
                window.location.href = '/cabinet';
            }
        })
        .catch(error => {
            console.log('Ошибка проверки авторизации:', error);
        });
});