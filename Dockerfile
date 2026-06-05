FROM python:3.12-slim

WORKDIR /app

# Одразу ставимо залежності
RUN pip install --no-cache-dir fastapi uvicorn pydantic[email]

# Копіюємо весь проєкт
COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]