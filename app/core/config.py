from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:secretpassword@db:5432/fastapi_db"
    
    # 🌟 ДОДАЙ ЦІ ТРИ РЯДКИ ДЛЯ JWT:
    SECRET_KEY: str = "super_secret_key_for_jwt_tokens_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Оце поле виправляє помилку!
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()