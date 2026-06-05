from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- PROFILE SCHEMAS ---
class ProfileBase(BaseModel):
    bio: Optional[str] = None
    phone: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    class Config: from_attributes = True

# --- ORDER SCHEMAS ---
class OrderCreate(BaseModel):
    item_name: str
    quantity: int

class OrderResponse(OrderCreate):
    id: int
    class Config: from_attributes = True

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # В реаліях хешується, тут для валідації

class UserResponse(UserBase):
    id: int
    profile: Optional[ProfileResponse] = None
    orders: List[OrderResponse] = []
    class Config: from_attributes = True