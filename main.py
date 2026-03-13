from fastapi import FastAPI, HTTPException
import re

import random
import pyd

app = FastAPI()

@app.post("/users")
def Users(user:pyd.UserCreate):
    emailRegex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(emailRegex, user.email):
        raise HTTPException(400, "Неверный формат почты")
    
    if not user.username.isalnum():
        raise HTTPException(400, "Неверный формат имени пользователя")
    
    if not (user.password.isalnum() & (not user.password.isdigit()) & (not user.password.isalpha())):
        raise HTTPException(400, "Неверный формат пароля")
    
    user.id = random.randint(0, 10000)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "age": user.age
    }
    
@app.post("/items")
def Items(item:pyd.ItemCreate):
    if len(item.tags) > 5:
        raise HTTPException(400, "Слишком много тегов")
    
    if not item.in_stock:
        item.quantity = 1

    return {
        "name": item.name,
        "description": item.description,
        "tags": item.tags,
        "quantity": item.quantity, 
        "price": item.price + item.price * item.tax / 100
    }

@app.post("/filter-users", response_model=pyd.ResponseFilters)
def Filter(filters:pyd.FilterUsers):
    if (filters.filters.min_age != None) & (filters.filters.max_age != None) & (filters.filters.max_age < filters.filters.min_age):
        raise HTTPException(400, "Мин. возраст больше максимального")
    
    result = pyd.ResponseFilters
    result.total_input = len(filters.users)
    result.applied_filters = filters.filters
    filtered_users = []

    for user in filters.users:
        if (filters.filters.min_age > user.age):
            continue

        if (filters.filters.max_age < user.age):
            continue

        if (filters.filters.is_active == None):
            filtered_users.append(user)
            continue

        if (filters.filters.is_active != user.active):
            continue

        filtered_users.append(user)

    
    result.filtered_users = filtered_users
    result.filtered_count = len(result.filtered_users)
    return result