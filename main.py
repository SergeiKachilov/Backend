from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
import datetime

app = FastAPI()
api_key = APIKeyHeader(name="x-api-key")
sec = HTTPBasic()

def CheckUser(login: str, password: str, session: SessionDep):
    user = session.exec(select(User).where(User.login == login)).first()
    if user is None:
        return False
    
    if not bcrypt.checkpw(password.encode(), user.password):
        return False
    
    return True

@app.get("/test")
def test1(api_token=Security(api_key)):
    if api_token != "abc123":
        raise HTTPException(403, "Неверный токен")
    return {"secret": "ВАЖНО"}

@app.get("/test")
def test2(session: SessionDep, creds:HTTPBasicCredentials=Depends(sec)):
    user = select(User).where(User.login == creds.username, User.password==creds.password)
    result = session.exec(user).first()
    if not result:
        raise HTTPException(403, "Неверный логин или пароль")
    return {"secret": "ВАЖНО"}

@app.post("/register")
def Register(session: SessionDep, newUser: RegUser):
    users = session.exec(select(User)).all()
    for user in users:
        if newUser.login.lower() == user.login.lower():
            raise HTTPException(400, "Пользователь с таким логином уже существует!")
    
    hashed = bcrypt.hashpw(newUser.password, bcrypt.gensalt())

    session.add(User(login=newUser.login, password=hashed))
    session.commit()

@app.get("/tasks", response_model=list[ResponseTask])
def GetTasks(session: SessionDep, page:int, creds:HTTPBasicCredentials=Depends(sec)):
    if not CheckUser(creds.username, creds.password, session):
        raise HTTPException(400, "Неверный логин или пароль!")
    user = session.exec(select(User).where(User.login == creds.username)).first()

    tasks = session.exec(select(Task, Priority, Status).where(Task.user_id == user.id).join(Priority).join(Status).offset(5*(page-1)).limit(5)).all()
    result = []

    for task, priority, status in tasks:
        if task.deadline is not None:
            task.deadline = datetime.datetime.fromtimestamp(task.deadline).strftime("%d.%m.%Y")

        result.append({"name": task.name, "description":task.description, "deadline": task.deadline, "priority": priority.name, "status": status.name})
    
    return result
