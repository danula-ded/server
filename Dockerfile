FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -g 10001 app && useradd -m -u 10001 -g 10001 app

RUN mkdir -p /app && chown -R app:app /app

WORKDIR /app/backend

RUN pip install --no-cache-dir \
    Django==5.1.5 \
    djangorestframework==3.15.2 \
    drf-spectacular==0.28.0 \
    psycopg[binary]==3.2.3 \
    prometheus-client==0.21.1

RUN pip install --no-cache-dir \
    pytest==8.3.4 \
    pytest-django==4.9.0 \
    ruff==0.8.6

COPY --chown=app:app backend /app/backend

USER app

EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
