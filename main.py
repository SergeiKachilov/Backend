from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep
from models import *

app = FastAPI()
api_key = APIKeyHeader(name="x-api-key")
sec = HTTPBasic()

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

