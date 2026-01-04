# Эксплуатация проекта (админка, env, БД, проверка требований)

## 1) Как войти в админку Django

### URL админки

- `http://localhost/admin/`

### Создание администратора (superuser)

Выполняется внутри контейнера `web`:

```bash
docker-compose exec web python manage.py createsuperuser
```

Далее введи `username`, `email` (можно пустым) и `password`.

### После создания

- Открой `http://localhost/admin/`
- Введи логин/пароль

## 2) Где находится env и откуда берутся значения в docker-compose

### Вариант A: переменные окружения ОС

`docker-compose` подставляет значения из твоего окружения (переменных Windows / терминала).

### Вариант B: файл `.env`

Docker Compose автоматически читает файл `.env`, если он лежит рядом с `docker-compose.yml`.

Сейчас `.env` **не обязателен**, потому что в `docker-compose.yml` стоят значения по умолчанию вида:

- `${DB_NAME:-app}`
- `${DJANGO_DEBUG:-1}`

То есть, если переменная не задана — будет использован дефолт.

Пример `.env`, если хочешь управлять значениями явно:

```env
DJANGO_SECRET_KEY=some-secret
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
LOG_LEVEL=INFO

DB_NAME=app
DB_USER=app
DB_PASSWORD=app
```

### Где эти значения читаются в Django

- `backend/config/env.py` — функции `get_env`, `get_bool`, `get_csv` читают **только** `os.environ`.
- `backend/config/settings.py` — получает настройки (DB, DEBUG, ALLOWED_HOSTS, LOG_LEVEL и т.д.) только через `get_env/get_bool/get_csv`.

## 3) Как посмотреть базу данных PostgreSQL

### Подключение через psql внутри контейнера БД

```bash
docker-compose exec database psql -U app -d app
```

Если ты переопределял `DB_USER/DB_NAME`, подставь свои значения.

Полезные команды внутри `psql`:

- `\dt` — список таблиц
- `\d example_app_exampleitem` — структура таблицы
- `select * from example_app_exampleitem;` — данные

### Где хранятся данные

Данные Postgres сохраняются в named volume `postgres_data`.

Полная очистка данных (осторожно):

```bash
docker-compose down -v
```

## 4) Как проверить, что выполнены базовые требования задания

### 4.1 Порядок контейнеров и доступный порт

- В compose используются контейнеры:
  - `database` (PostgreSQL)
  - `web` (Django)
  - `nginx` (reverse proxy)

Проверить запущенные контейнеры:

```bash
docker-compose ps
```

Порт наружу должен быть только один — `80` у `nginx`.

### 4.2 Healthcheck на все контейнеры

В `docker-compose.yml` настроены `healthcheck` для:

- `database` (pg_isready)
- `web` (HTTP запрос на `/health/`)
- `nginx` (wget на `/health/` через nginx)

Проверить статус:

```bash
docker-compose ps
```

Статус должен быть `healthy`.

### 4.3 Проверка `/health/`

Открой:

- `http://localhost/health/`

Должно вернуть `200`.

### 4.4 Correlation-ID middleware + формат логов

Как проверить вручную:

1) Сделай запрос с заголовком `X-Correlation-ID`.
2) Посмотри логи `web`.

Пример (PowerShell):

```powershell
Invoke-WebRequest http://localhost/health/ -Headers @{"X-Correlation-ID"="test-123"}
```

Логи:

```bash
docker-compose logs -f web
```

Ожидаемый формат:

- `[test-123] <log message>`

Если заголовок не передан — middleware генерирует UUID.

### 4.5 Middleware метрик (Counter) + просмотр метрик

Счётчики запросов реализованы через Prometheus-compatible `Counter`:

- `http_requests_total`
- `http_responses_2xx_total`
- `http_responses_4xx_total`
- `http_responses_5xx_total`

Для просмотра добавлен endpoint:

- `http://localhost/metrics/`

Проверь так:

1) Несколько раз открой `/health/`.
2) Открой `/metrics/` и найди счётчики выше — значения должны увеличиваться.

### 4.6 Latency Histogram

Инструмент реализован в `backend/core/metrics.py`:

- декоратор `track_latency(operation: str)`
- метрика `integration_latency_seconds` (Histogram)

Чтобы histogram начал появляться/наполняться в `/metrics/`, нужно применить декоратор к реальному коду (например, к функции, делающей запрос к БД).

## 5) Тесты и линтер

### Pytest (интеграционный тест /health)

```bash
docker-compose exec web pytest -q
```

Ожидается прохождение теста `backend/tests/test_health.py`.

### Ruff (линтер)

```bash
docker-compose exec web ruff check .
```

Если ruff предлагает авто-фикс:

```bash
docker-compose exec web ruff check --fix .
docker-compose exec web ruff check .
```

## 6) Оценка соответствия экзаменационному ТЗ

Ниже оценка по тексту задания.

### Docker / compose

- **Не запускать контейнеры от root**: выполнено для `web` и `nginx`. Для `database` используется пользователь `postgres` (это не `root`).
- **Healthcheck на все контейнеры**: выполнено.
- **Контейнеры и порядок**: `database` → `web` → `nginx` (через `depends_on: condition: service_healthy`).
- **Volume для кода (dev)**: есть `./backend:/app/backend`.
- **Volume для данных БД**: есть `postgres_data`.
- **Наружу открыт только порт 80 у nginx**: выполнено.
- **Требование про компилируемый язык**: не применимо (Python).

### Backend

- **Histogram latency инструмент**: реализован (`track_latency`, `Histogram`).
- **Middleware счётчиков**: реализован (Prometheus Counters).
- **Отдельный конфигурационный модуль env**: реализован (`config/env.py`).
- **Correlation-ID middleware + формат логов**: реализовано.
- **Интеграционный тест пустого endpoint `/health/` и 200**: реализован.
- **Ruff**: настроен в `backend/pyproject.toml`.

### Важное замечание

В проект также добавлены расширения (регистрация/JWT, фильтры/поиск/пагинация), которые **не требуются экзаменационным ТЗ**. Если нужно строгое соответствие сдаче, их лучше удалить (см. `GUIDE.md` раздел «Как удалить расширения»).
