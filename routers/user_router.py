from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler

router = APIRouter(prefix="/v1/user", tags=["User"])
auth_handler = AuthHandler()

@router.post("/register")
def Register(session: SessionDep, newUser: RegUser):
    users = session.exec(select(User)).all()
    for user in users:
        if newUser.login.lower() == user.login.lower():
            raise HTTPException(400, "Пользователь с таким логином уже существует!")

    hashed = bcrypt.hashpw(bytes(newUser.password, "utf-8"), bcrypt.gensalt())

    session.add(User(login=newUser.login, password=hashed))
    session.commit()

    return {"message": "success"}

@router.post("/login")
def Login(user_input: RegUser, session: SessionDep):
    user = session.exec(select(User).where(User.login==user_input.login)).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    if auth_handler.verify_password(user_input.password, user.password):
        token = auth_handler.encode_token(user.login)
        return {"token": token}
    else:
        raise HTTPException(403, "Неверный пароль")