# Django Backend Template Guide

## Быстрый старт

- Основной запуск (экзаменационный режим, наружу открыт только порт 80 через nginx):

```bash
docker-compose up --build
```

Если команда `docker-compose up --build` завершается со словом `canceled`, это обычно значит, что запуск был прерван (например, Ctrl+C). Для запуска в фоне используй:

```bash
docker-compose up -d --build
```

## Эндпоинты

- `/health/` — healthcheck, должен возвращать 200
- `/docs/` — Swagger UI
- `/docs/schema/` — OpenAPI schema
- `/api/items/` — эталонный CRUD (DRF ModelViewSet)

## Аутентификация (важно)

В текущей конфигурации:

- `/health/` и `/docs/` доступны без токена
- `/api/auth/*` доступно без токена (регистрация и получение токенов)
- остальные `/api/*` по умолчанию требуют JWT (`IsAuthenticated`)

## Как добавить новую сущность (пример)

### 1) Создать модель

Создай новое приложение или скопируй `example_app` (как шаблон).
Минимальный путь:

- `backend/<new_app>/models.py`
- `backend/<new_app>/serializers.py`
- `backend/<new_app>/views.py`
- `backend/<new_app>/urls.py`

### 2) Добавить Serializer

Используй `ModelSerializer`.

### 3) Добавить ViewSet

Используй `ModelViewSet`.

### 4) Подключить роуты

Через `DefaultRouter()` и `include(router.urls)`.

### 5) Миграции

Внутри контейнера:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Как новый endpoint появляется в Swagger

Swagger генерируется автоматически через **drf-spectacular**.
Чтобы endpoint появился в `/docs/`:

- он должен быть подключён в `urlpatterns` (прямо или через `include()`)
- для DRF view/viewset должна быть доступна схема (по умолчанию она есть)

Ничего «генерировать вручную» не нужно: `/docs/schema/` строится динамически.

## Проверки (pytest / ruff)

```bash
docker-compose exec web pytest -q
docker-compose exec web ruff check .
```

Если ruff предлагает авто-фикс:

```bash
docker-compose exec web ruff check --fix .
```

## Пагинация, поиск, сортировка, фильтры

### Где включено

Глобально в `backend/config/settings.py`:

- пагинация: `PageNumberPagination`
- фильтры: `django-filter`
- поиск: `SearchFilter`
- сортировка: `OrderingFilter`

На примере `ExampleItemViewSet`:

- `filterset_fields = ["name"]`
- `search_fields = ["name"]`
- `ordering_fields = [...]`

Примеры запросов:

- фильтр: `/api/items/?name=Test`
- поиск: `/api/items/?search=Test`
- сортировка: `/api/items/?ordering=-id`
- пагинация: `/api/items/?page=2`

## JWT / регистрация (добавлено как расширение)

Эндпоинты:

- `POST /api/auth/register/` — регистрация пользователя (`username`, `password`)
- `POST /api/auth/token/` — получить `access` и `refresh`
- `POST /api/auth/token/refresh/` — обновить `access` по `refresh`

### Как использовать

1) Зарегистрировать пользователя:

```bash
curl -X POST http://localhost/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password123"}'
```

2) Получить токены:

```bash
curl -X POST http://localhost/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password123"}'
```

3) Использовать access-токен:

```bash
curl http://localhost/api/items/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Как удалить расширения (JWT + фильтры)

### Удалить JWT/регистрацию

- удалить папку `backend/auth_app/`
- удалить строку `"auth_app",` из `INSTALLED_APPS` в `backend/config/settings.py`
- удалить строку `path("api/auth/", include("auth_app.urls")),` из `backend/config/urls.py`
- удалить зависимость `djangorestframework-simplejwt` из `Dockerfile`
- (опционально) удалить блок `SIMPLE_JWT` из `backend/config/settings.py`

### Удалить фильтры/поиск/пагинацию

- удалить `django-filter` из `Dockerfile`
- удалить `"django_filters",` из `INSTALLED_APPS`
- удалить `DEFAULT_FILTER_BACKENDS`, `DEFAULT_PAGINATION_CLASS`, `PAGE_SIZE` из `REST_FRAMEWORK`
- удалить `filterset_fields/search_fields/ordering_fields` из `ExampleItemViewSet`
