from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List

from ..db.session import get_db
from ..models.user import User, Profile, Order
from ..models.product import Category, Product
from ..schemas.user import UserCreate, UserResponse, OrderCreate, OrderResponse, ProfileCreate, ProfileResponse
from ..schemas.product import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse

router = APIRouter(tags=["E-Commerce API"])

# --- 1. USER CRUD ---
@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(username=user_data.username, email=user_data.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/users/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    # Використовуємо selectinload для асинхронного завантаження зв'язків One-to-One та One-to-Many
    result = await db.execute(select(User).options(selectinload(User.profile), selectinload(User.orders)))
    return result.scalars().all()

# --- 2. PROFILE ROUTE (One-to-One) ---
@router.post("/users/{user_id}/profile", response_model=ProfileResponse)
async def create_user_profile(user_id: int, profile_data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    
    new_profile = Profile(**profile_data.model_dump(), user_id=user_id)
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

# --- 3. ORDER ROUTE (One-to-Many) ---
@router.post("/users/{user_id}/orders", response_model=OrderResponse)
async def create_order(user_id: int, order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(**order_data.model_dump(), user_id=user_id)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

# --- 4. CATEGORIES & PRODUCTS ROUTES ---
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