from fastapi import FastAPI
from .api.user import router as users_router

app = FastAPI(title="FastAPI CRUD", version="1.0.0")

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI CRUD App (Variant 1). Go to /docs for Swagger UI."}