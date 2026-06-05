from pydantic import BaseModel
from typing import List

class ProductCreate(BaseModel):
    title: str
    price: float

class ProductResponse(ProductCreate):
    id: int
    category_id: int
    class Config: from_attributes = True

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int
    products: List[ProductResponse] = []
    class Config: from_attributes = True