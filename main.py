from fastapi import FastAPI
import os
import psycopg2

app = FastAPI(title="FastAPI + Postgres Template")

@app.get("/")
def read_root():
    # Пробуємо підключитися до бази для перевірки
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fastapi_db")
    status = "disconnected"
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        status = "connected"
    except Exception as e:
        status = f"error: {str(e)}"

    return {
        "status": "working",
        "database": status,
        "message": "Hello World from Dockerized FastAPI!"
    }