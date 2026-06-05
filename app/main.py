from fastapi import FastAPI
from .api.user import router as api_router

app = FastAPI(title="FastAPI Async Postgres & Alembic Lab 4", version="2.0.0")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Lab 4 Connected to Async Postgres via SQLAlchemy 2.0 & Alembic."}