# API для лендинга (pitchcv.app)

Документация по интеграции лендинга **pitchcv.app** с бэкендом **my.pitchcv.app**.

---

## Домены

| Назначение | Домен |
|------------|-------|
| **Сайт / лендинг** | **pitchcv.app** |
| **Бэкенд (обработка, API)** | **my.pitchcv.app** |

Все запросы к API отправляются на `https://my.pitchcv.app`. CORS на бэкенде должен разрешать запросы с `pitchcv.app` и `www.pitchcv.app` (см. раздел 3).

---

## Выбранный поток (лендинг)

**На лендинге после загрузки результат не показываем.** Последовательность: данные загружаются → пользователь переходит на логин → после входа попадает сразу на **экран обработки** с уже запущенным анализом. Согласование с бекендом в процессе; после обновления API документ будет актуализирован.

---

## Два сценария (API)

1. **Бесплатная проверка без входа** — эндпоинт **POST /api/landing/analyze**: сразу возвращает ATS score и подсказки. Один запрос на IP за 24 часа.
2. **Загрузить файлы → войти → увидеть анализ в приложении** — эндпоинт **POST /api/landing/save**: сохраняет резюме и вакансию, возвращает токен; лендинг перенаправляет на `https://my.pitchcv.app/login?pending=TOKEN`. На странице логина показываются название файла и ссылка на вакансию с лоадерами; после входа (Google или email) пользователь попадает в приложение, данные подставляются и сразу запускается анализ.

Ниже — описание обоих эндпоинтов и настройка.

---

## 1. Бесплатная проверка (без входа): POST /api/landing/analyze

**POST** `https://my.pitchcv.app/api/landing/analyze`

(Для локальной разработки: `http://localhost:8000/api/landing/analyze`)

**Content-Type:** `multipart/form-data`

### Параметры (form fields)

| Поле         | Тип    | Обязательное | Описание |
|-------------|--------|--------------|----------|
| `resume`    | file   | да*          | Файл резюме: PDF, DOCX или текстовый файл. Макс. 5 МБ. |
| `resume_text` | string | да*        | Альтернатива файлу — резюме вставлено текстом. Макс. 50 000 символов (настраивается). |
| `job_url`   | string | да**         | Ссылка на вакансию (одна конкретная вакансия, не страница поиска). Макс. 2048 символов. |
| `job_text`  | string | да**         | Альтернатива ссылке — текст вакансии вставлен вручную. |

\* Нужно одно из двух: либо `resume`, либо `resume_text`.  
\** Нужно одно из двух: либо `job_url`, либо `job_text`.

### Ответ (200 OK)

JSON в формате ответа `/api/analyze`:

```json
{
  "ats_score": 72,
  "keyword_score": 0.65,
  "keyword_threshold": 0.25,
  "job": {
    "title": "Software Engineer",
    "company": "Company Name",
    "requirements": ["..."],
    "keywords": ["..."],
    "description": "..."
  },
  "recommendations": [
    { "category": "Ключевые слова", "labels": ["Python", "SQL"] },
    { "category": "Структура", "labels": ["В порядке"] },
    { "category": "Требования", "labels": ["Явно укажите соответствие требованиям..."] }
  ],
  "skills_score": 70,
  "experience_score": 75,
  "portfolio_score": null,
  "improvement_tips": "### Рекомендации\n\n..."
}
```

- **ats_score** — оценка ATS 0–100.
- **keyword_score** — доля совпадения ключевых слов (0–1).
- **job** — распарсенная вакансия (заголовок, компания, требования, ключевые слова).
- **recommendations** — три категории: ключевые слова, структура, требования (что улучшить).
- **improvement_tips** — текст с рекомендациями от LLM (можно показать блоком под результатами).

### Ошибки

| Код | Причина |
|-----|--------|
| 400 | Нет резюме или вакансии, пустой текст, слишком длинный текст/URL. |
| 422 | Ссылка на страницу поиска, а не на вакансию; не удалось загрузить вакансию по URL. |
| 429 | Лимит: одна проверка на IP в течение N часов (по умолчанию 24). Текст: «Одна бесплатная проверка на 24 часа. Зарегистрируйтесь на my.pitchcv.app для неограниченного доступа.» |
| 503 | Не настроен GOOGLE_API_KEY или сервис временно недоступен. |

---

## 2. Сохранить и перейти на логин: POST /api/landing/save

Сценарий: пользователь на лендинге загружает файл резюме и ссылку на вакансию, жмёт кнопку «Проверить» → бэкенд сохраняет данные и возвращает одноразовый токен → лендинг перенаправляет на `https://my.pitchcv.app/login?pending=TOKEN`. На странице логина отображаются название файла и ссылка на вакансию с лоадерами; после входа (Google или email) пользователь попадает в приложение на страницу оптимизации, данные подставляются и сразу запускается анализ.

**POST** `https://my.pitchcv.app/api/landing/save`

**Content-Type:** `multipart/form-data`

Параметры — те же, что у `/api/landing/analyze`: `resume` или `resume_text`, и `job_url` или `job_text`.

### Ответ (200 OK)

```json
{
  "token": "abc123...",
  "resume_filename": "resume.pdf",
  "job_url": "https://example.com/job/123",
  "job_title": "Software Engineer"
}
```

- **token** — передать в URL редиректа: `https://my.pitchcv.app/login?pending=TOKEN`. Срок жизни токена задаётся `LANDING_PENDING_TTL_SECONDS` (по умолчанию 900, т.е. 15 минут).
- **resume_filename**, **job_url**, **job_title** — для отображения на лендинге до редиректа (опционально).

После редиректа на логин приложение само запрашивает **GET /api/landing/pending?token=TOKEN** (без авторизации) и показывает блок «Ваши файлы готовы к анализу» с названием файла и ссылкой. После входа вызывается **GET /api/landing/claim?token=TOKEN** (с авторизацией), данные подставляются в форму и запускается анализ.

### Ошибки

Те же коды, что у `/api/landing/analyze` (400, 422 и т.д.). Rate limit по IP к save не применяется (лимит только у analyze).

---

## 3. CORS

Бэкенд разрешает запросы только с доменов, перечисленных в **LANDING_ALLOWED_ORIGINS** (см. раздел «Настройка бэкенда»). По умолчанию туда нужно добавить:

- `https://pitchcv.app`
- `https://www.pitchcv.app`

Для локальной разработки лендинга добавьте, при необходимости, `http://localhost:PORT`.

---

## 4. Антифрод и лимиты

- **Один запрос на IP за N часов** (по умолчанию 24). Хранится in-memory на бэкенде; при нескольких инстансах нужен Redis (можно доработать).
- **Максимальный размер резюме:** 50 000 символов (текст после извлечения из PDF/DOCX). Настраивается через `LANDING_MAX_RESUME_CHARS`.
- **Максимальный размер файла резюме:** 5 МБ.
- **Максимальная длина job_url:** 2048 символов (`LANDING_MAX_JOB_URL_LEN`).
- Данные резюме и вакансии **не сохраняются** в историю и не привязываются к пользователю.
- Рекомендуется на лендинге: скрытое поле (honeypot), при заполнении — не отправлять запрос; по желанию — reCAPTCHA перед отправкой.

---

## 5. Пример запроса с лендинга (JavaScript)

```javascript
const formData = new FormData();
formData.append("resume", fileInput.files[0]);  // или formData.append("resume_text", textarea.value);
formData.append("job_url", jobUrlInput.value);  // или formData.append("job_text", jobTextarea.value);

const response = await fetch("https://my.pitchcv.app/api/landing/analyze", {
  method: "POST",
  body: formData,
  credentials: "omit",
});

if (response.status === 429) {
  const data = await response.json().catch(() => ({}));
  alert(data.detail || "Одна бесплатная проверка на 24 часа. Зарегистрируйтесь на my.pitchcv.app.");
  return;
}

if (!response.ok) {
  const err = await response.json().catch(() => ({}));
  throw new Error(err.detail || response.statusText);
}

const result = await response.json();
// result.ats_score, result.recommendations, result.improvement_tips, result.job
```

### Пример curl (файл + ссылка на вакансию)

```bash
curl -X POST "https://my.pitchcv.app/api/landing/analyze" \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_url=https://example.com/job/123"
```

### Пример curl (текст резюме + текст вакансии)

```bash
curl -X POST "https://my.pitchcv.app/api/landing/analyze" \
  -F "resume_text=John Doe, Software Engineer..." \
  -F "job_text=We are looking for a Software Engineer..."
```

---

## 6. Настройка бэкенда (.env или Service Variables)

На сервере (my.pitchcv.app) должны быть заданы:

```env
# Обязательно для анализа
GOOGLE_API_KEY=...

# Допустимые домены для CORS (через запятую, без пробелов внутри URL)
LANDING_ALLOWED_ORIGINS=https://pitchcv.app,https://www.pitchcv.app

# Лимит: 1 проверка на IP за N часов
LANDING_RATE_LIMIT_HOURS=24

# Макс. длина текста резюме (символов)
LANDING_MAX_RESUME_CHARS=50000

# Макс. длина ссылки на вакансию (символов)
LANDING_MAX_JOB_URL_LEN=2048

# TTL токена «save → login» (секунды). По умолчанию 15 мин.
LANDING_PENDING_TTL_SECONDS=900
```

После изменения `LANDING_ALLOWED_ORIGINS` бэкенд нужно перезапустить.

---

## 7. Что показывать на лендинге

Рекомендуемый минимум:

1. **Match score (ATS)** — `result.ats_score` (0–100) и, при желании, `result.keyword_score` (например, в процентах).
2. **Вакансия** — `result.job.title`, `result.job.company` для подписи «Проверка по вакансии: …».
3. **Что улучшить** — `result.recommendations` (три категории с списками лейблов).
4. **Подсказки** — `result.improvement_tips` (Markdown или простой текст).
5. При 429 — сообщение про одну проверку в 24 часа и призыв зарегистрироваться на my.pitchcv.app.

Ссылку на приложение для полного функционала: **https://my.pitchcv.app**.

---

## 8. Сводка для фронта лендинга

- **Быстрая проверка без входа:** `POST https://my.pitchcv.app/api/landing/analyze` — формат `multipart/form-data`, ответ как у `/api/analyze`. Лимит: 1 запрос на IP за 24 часа.
- **Переход в приложение с файлами:** `POST https://my.pitchcv.app/api/landing/save` — те же поля; ответ `{ token, resume_filename, job_url, job_title }`. Редирект на `https://my.pitchcv.app/login?pending=TOKEN`. После входа пользователь попадает в приложение с подставленными данными и запуском анализа.
