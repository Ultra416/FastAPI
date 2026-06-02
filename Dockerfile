FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]