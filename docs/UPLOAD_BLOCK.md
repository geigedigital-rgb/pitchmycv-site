# Блок «Upload zone» (форма загрузки резюме + вакансия)

Официальное название блока в проекте для передачи разработчикам: **Upload zone** или **compact upload card**.

## Что это

Один блок с функционалом:
- **Шаг 1:** загрузка файла резюме (drag & drop или выбор), PDF/DOC/DOCX, макс. 5 МБ.
- **Шаг 2:** поле для вставки текста вакансии (textarea).
- Справа внизу: шкала «0% · Interview chances» и кнопка **Check your resume now**.

По нажатию кнопки вызывается **POST /api/landing/save** (resume + job_text), затем редирект на `my.pitchcv.app/login?pending=TOKEN`. Подробнее — в [LANDIND_API.md](./LANDIND_API.md).

## Где лежит в проекте

| Что | Где |
|-----|-----|
| **HTML блока** | `index.html` — контейнер с `id="upload-zone"` и классом `compact-upload-card` (секция hero, примерно строки 143–211). |
| **Стили** | `css/style.css` — классы `.compact-upload-card`, `.compact-upload-row`, `.compact-file-card`, `.compact-dropzone`, `.compact-link-card`, `.compact-upload-bottom`, `.compact-gauge`, `.upload-job-textarea` и др. |
| **Логика** | `js/main.js` — обработчики для `#upload-zone`, `#file-input`, `#upload-dropzone`, `#job-text-input`, `#analyze-resume-btn`: выбор файла, включение шага 2, отправка формы, оверлей загрузки, редирект. |

## Как вставить блок на другую страницу

1. **Скопировать разметку** — из `index.html` весь блок от `<div class="compact-upload-card" id="upload-zone" ...>` до закрывающего `</div>` (внутри hero-right). Сохранить все `id`: `upload-zone`, `file-input`, `upload-dropzone`, `job-link-step`, `job-text-input`, `job-link-note`, `analyze-resume-btn`, `dropzone-title`, `dropzone-help`, `file-step-status`.
2. **Подключить стили** — на странице должен быть подключён `css/style.css` (или тот же набор правил для compact-upload и связанных классов).
3. **Подключить скрипт** — на странице должен быть подключён `js/main.js` (в нём логика для `#upload-zone` и кнопки). Если блок вставляется на страницу без hero, убедиться, что в DOM есть один элемент с `id="upload-zone"`.

## Ключевые id и классы

- Контейнер: `id="upload-zone"`, класс `compact-upload-card`
- Файл: `id="file-input"` (hidden), `id="upload-dropzone"` (зона клика/drag)
- Вакансия: `id="job-text-input"` (textarea), `id="job-link-step"` (секция)
- Кнопка: `id="analyze-resume-btn"`
- Подсказки: `id="dropzone-title"`, `id="dropzone-help"`, `id="file-step-status"`, `id="job-link-note"`

Использование другого `id` для контейнера потребует правок в `main.js` (селектор `getElementById("upload-zone")` и привязка оверлея загрузки).
