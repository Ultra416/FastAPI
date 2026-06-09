from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db, get_current_user
from app.models.user import User, Profile, Order
from app.models.product import Category, Product
from app.schemas.user import UserCreate, UserResponse, OrderCreate, OrderResponse, ProfileCreate, ProfileResponse
from app.schemas.product import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Auth & Protected E-Commerce"])

# --- 1. РУЧКА РЕЄСТРАЦІЇ (REGISTRATION) ---
@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Хешуємо та солимо пароль
    secured_password = hash_password(user_data.password)
    
    new_user = User(
        username=user_data.username, 
        email=user_data.email, 
        hashed_password=secured_password
    )
    db.add(new_user)
    await db.commit()
    
    # 🌟 ФІКС: Завантажуємо об'єкт заново разом із зв'язками для безпечної валідації відповіді
    query = (
        select(User)
        .where(User.id == new_user.id)
        .options(selectinload(User.profile), selectinload(User.orders))
    )
    refresh_result = await db.execute(query)
    return refresh_result.scalar_one()


# --- 2. РУЧКА АВТЕНТИФІКАЦІЇ (LOGIN ТА ВСТАНОВЛЕННЯ COOKIES) ---
@router.post("/login")
async def login(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    # Перевіряємо наявність юзера та валідність соленого пароля
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Створюємо JWT токен
    access_token = create_access_token(data={"sub": user.email})
    
    # Записуємо токен у безпечні HTTP-only Cookies
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,       # Захист від XSS
        max_age=1800,        # 30 хвилин
        samesite="lax"
    )
    
    return {"message": "Successfully logged in"}


# --- 3. ЗАХИЩЕНА РУЧКА: СТВОРЕННЯ ЗАМОВЛЕННЯ (Вимагає авторизації) ---
@router.post("/orders/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Захист через Depends
):
    new_order = Order(**order_data.model_dump(), user_id=current_user.id)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


# --- 4. ЗАХИЩЕНА РУЧКА: ПЕРЕГЛЯД ВЛАСНИХ ЗАМОВЛЕНЬ ---
@router.get("/orders/my", response_model=List[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Захист через Depends
):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalars().all()


# --- 5. РУЧКА ВИХОДУ (LOGOUT) ---
@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


# --- Існуючі ручки категорій (залишаємо для роботи маркетплейсу) ---
@router.post("/categories/", response_model=CategoryResponse)
async def create_category(cat: CategoryCreate, db: AsyncSession = Depends(get_db)):
    new_cat = Category(name=cat.name)
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat

@router.post("/categories/{category_id}/products", response_model=ProductResponse)
async def create_product(category_id: int, prod: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_prod = Product(**prod.model_dump(), category_id=category_id)
    db.add(new_prod)
    await db.commit()
    await db.refresh(new_prod)
    return new_prod

@router.get("/categories/", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).options(selectinload(Category.products)))
    return result.scalars().all()