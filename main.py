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