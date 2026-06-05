from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

users_db = {}
id_counter = 1

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    global id_counter
    
    # Імітуємо перевірку унікальності email
    for u in users_db.values():
        if u["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    new_user = {
        "id": id_counter,
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name
    }
    users_db[id_counter] = new_user
    id_counter += 1
    return new_user

@router.get("/", response_model=List[UserResponse])
def get_users():
    return list(users_db.values())

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
        
    current_user = users_db[user_id]
    current_user["username"] = user_data.username
    current_user["email"] = user_data.email
    current_user["full_name"] = user_data.full_name
    
    users_db[user_id] = current_user
    return current_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None