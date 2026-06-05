from __future__ import annotations

from fastapi import Request, HTTPException, Depends, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Чисті абсолютні імпорти:
from app.core.config import settings
from app.db.base_class import Base

# Налаштування підключення
engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# ГЕНЕРАТОР СЕСІЙ ДЛЯ РУЧОК
async def get_db():
    async with async_session() as session:
        yield session

# 🌟 ЗАЛЕЖНІСТЬ ДЛЯ АВТОРИЗАЦІЇ ЧЕРЕЗ COOKIES
async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    # 1. Дістаємо токен з безпечних Cookies
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # 2. Декодуємо JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    # Імпортуємо локально всередині функції, щоб уникнути зациклення!
    from app.models.user import User
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    return user