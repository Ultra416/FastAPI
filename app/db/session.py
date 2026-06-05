from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..core.config import settings
from sqlalchemy.orm import DeclarativeBase

# Створюємо асинхронний двигун
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовий клас для всіх моделей
class Base(DeclarativeBase):
    pass

# Залежність (Dependency) для отримання сесії в роутерах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session