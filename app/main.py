from fastapi import FastAPI
from .api.user import router as api_router

app = FastAPI(title="FastAPI Async Postgres & JWT Auth Lab 5", version="3.0.0")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Lab 5 Protected API with JWT Tokens & HTTP-only Cookies is running."}