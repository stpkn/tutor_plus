// timetable.js — динамическое расписание (под твои кнопки и верстку)

let currentDate = new Date();
const DOW = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'];
const RU_DOW = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье'];

function pad(n){ return n.toString().padStart(2,'0'); }
const MONTHS_GEN = [
  'января','февраля','марта','апреля','мая','июня',
  'июля','августа','сентября','октября','ноября','декабря'
];

function fmtDateTitle(d){
  const weekday = RU_DOW[(d.getDay()+6)%7].toLowerCase(); // понедельник, вторник...
  const day = d.getDate();                                // без ведущего нуля
  const month = MONTHS_GEN[d.getMonth()];                 // РОДИТЕЛЬНЫЙ падеж
  const year = d.getFullYear();
  return `${weekday}, ${day} ${month} ${year} г.`;
}
function toDowName(d){
  // JS: Sunday=0..Saturday=6 → monday..sunday
  const js = d.getDay();
  return DOW[(js + 6) % 7];
}

async function loadScheduleForCurrentDay(){
  // заголовок с датой
  const titleEl = document.getElementById('currentPeriod');
  if (titleEl) titleEl.textContent = fmtDateTitle(currentDate);

  // таблица
  const body = document.getElementById('schedule-body');
  if (!body) return;
  body.innerHTML = `<tr><td colspan="3" style="padding:16px;">Загрузка…</td></tr>`;

  try {
    const res = await fetch('/api/schedule', {credentials:'same-origin'});
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const all = data.schedule || [];

    const dow = toDowName(currentDate);
    const items = all
      .filter(s => (s.day_of_week || '').toLowerCase() === dow)
      .sort((a,b) => (a.start_time > b.start_time ? 1 : -1));

    if (items.length === 0) {
      body.innerHTML = `<tr><td colspan="3" style="padding:16px;">Нет занятий на выбранный день</td></tr>`;
      return;
    }

    body.innerHTML = items.map(s => {
      const time = `${(s.start_time||'').slice(0,5)} — ${(s.end_time||'').slice(0,5)}`;
      const fullName = [s.student_name, s.student_last_name].filter(Boolean).join(' ') || 'Ученик';
      const topic = s.topic_title || 'Занятие';
      const exam = (s.exam_type || '').toLowerCase(); // если вернется с бэка

      // классы и верстка под твой стиль
      return `
        <tr class="schedule-row">
          <td class="time-slot">${time}</td>
          <td>
            <div class="lesson-card ${exam}">
              <div class="lesson-header">
                <div class="student-info">
                  <div class="student-avatar">${
                    fullName ? fullName.split(' ').map(w => w[0]||'').join('').slice(0,2).toUpperCase() : 'У'
                  }</div>
                  <div class="student-details">
                    <h4>${fullName}</h4>
                    <p>${(s.grade ? s.grade + ' класс • ' : '') + (s.exam_type ? s.exam_type.toUpperCase() : '')}</p>
                  </div>
                </div>
                <span class="lesson-type ${exam}">${s.exam_type ? s.exam_type.toUpperCase() : ''}</span>
              </div>
              <div class="lesson-details">
                <div class="lesson-topic">${topic}</div>
                <div class="lesson-description">${s.lesson_link ? `Ссылка: ${s.lesson_link}` : ''}</div>
              </div>
              <div class="lesson-actions">
                <button class="btn-small btn-start">Начать</button>
                <button class="btn-small btn-edit">✏️</button>
              </div>
            </div>
          </td>
          <td class="actions-col">
            <!-- при желании продублировать кнопки -->
          </td>
        </tr>
      `;
    }).join('');

  } catch (e) {
    console.error('Ошибка загрузки расписания:', e);
    body.innerHTML = `<tr><td colspan="3" style="padding:16px;">Не удалось загрузить расписание</td></tr>`;
  }
}

// Эти функции вызываются из HTML через onclick
window.previousDay = function(){
  currentDate.setDate(currentDate.getDate() - 1);
  loadScheduleForCurrentDay();
}
window.nextDay = function(){
  currentDate.setDate(currentDate.getDate() + 1);
  loadScheduleForCurrentDay();
}

// Первичная загрузка (и защита от неавторизованных)
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/check-auth')
    .then(r => r.json())
    .then(j => j.authenticated ? loadScheduleForCurrentDay()
                                : window.location.assign('/cabinet'))
    .catch(() => loadScheduleForCurrentDay());
});
