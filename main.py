from fastapi import FastAPI, HTTPException
import re

import random
import pyd

app = FastAPI()

users = []

@app.post("/users", response_model=pyd.ResponseUser)
def Users(user:pyd.UserCreate):
    emailRegex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if not re.fullmatch(emailRegex, user.email):
        raise HTTPException(400, "Неверный формат почты")
    
    if not user.username.isalnum():
        raise HTTPException(400, "Неверный формат имени пользователя")
    
    if not (user.password.isalnum() & (not user.password.isdigit()) & (not user.password.isalpha())):
        raise HTTPException(400, "Неверный формат пароля")
    
    ids = []

    for userItem in users:
        ids.append(userItem.id)
    
    user.id = random.randint(0, 10000)

    while user.id in ids:
        user.id = random.randint(0, 10000)

    ids.append(user.id)
    users.append(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "age": user.age
    }
    
@app.post("/items", response_model=pyd.ResponseItem)
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

@app.post("/users/{user_id}", response_model=pyd.ResponseUser)
def Update(info:pyd.UserUpdate, user_id:int):
    user = pyd.UserCreate
    
    if (info.age > 0) & (info.age < 18):
        raise HTTPException(400, "Возраст меньше 18")
    
    flag = False
    for us in users:
        if us.id == user_id:
            user = us
            flag = True

    if not flag:
        raise HTTPException(400, "id пользователя не найден")
    
    emailRegex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
    if (not re.fullmatch(emailRegex, info.email)) & (info.email != ""):
        raise HTTPException(400, "Неверный формат почты")
    
    
    user.email = info.email if info.email != "" else user.email
    user.full_name = info.full_name if info.full_name != "" else user.full_name
    user.age = info.age if info.age != 0 else user.age
    user.is_active = info.is_active if info.is_active != None else user.is_active

    return user