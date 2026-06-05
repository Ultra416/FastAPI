from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    # Pydantic автоматично зчитає ці змінні з .env або docker-compose
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/fastapi_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()