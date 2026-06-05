FROM python:3.12-slim

WORKDIR /app

# Нам потрібні fastapi, uvicorn, pydantic-settings, alembic та асинхронний драйвер asyncpg
RUN pip install --no-cache-dir fastapi uvicorn pydantic[email] pydantic-settings alembic sqlalchemy asyncpg pyjwt bcrypt python-multipart

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]