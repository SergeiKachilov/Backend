from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep
from models import *
from enum import Enum
import bcrypt
import datetime
import routers
from auth import AuthHandler

router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])
sec = HTTPBasic()
auth_handler = AuthHandler()

class Filter(str, Enum):    
    in_progress = "In Progress"
    completed = "Completed"
    cancelled = "Cancelled"


def CheckUser(login: str, password: str, session: SessionDep):
    user = session.exec(select(User).where(User.login == login)).first()
    if user is None:
        return False

    if not bcrypt.checkpw(password.encode(), user.password):
        return False

    return True

@router.get("/", response_model=list[ResponseTask])
def GetTasks(
    session: SessionDep,
    page: int,
#     creds: HTTPBasicCredentials = Depends(sec),
    status_filter: Filter = None,
    deadline_sort: bool = False,
    username=Depends(auth_handler.auth_wrapper)
):
#     if not CheckUser(creds.username, creds.password, session):
#         raise HTTPException(400, "Неверный логин или пароль!")
    user = session.exec(select(User).where(User.login == username)).first()

    cmnd = (
        select(Task, Priority, Status)
        .where(Task.user_id == user.id)
        .join(Priority)
        .join(Status)
    )

    if status_filter is not None:
        cmnd = cmnd.where(Status.name == status_filter)

    if deadline_sort:
        cmnd = cmnd.order_by(Task.deadline)

    el_on_pages = 3
    cmnd = cmnd.offset(el_on_pages * (page - 1)).limit(el_on_pages)

    tasks = session.exec(cmnd).all()
    result = []

    for task, priority, status in tasks:
        if task.deadline is not None:
            task.deadline = datetime.datetime.fromtimestamp(task.deadline).strftime(
                "%d.%m.%Y"
            )

        result.append(
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "deadline": task.deadline,
                "priority": priority.name,
                "status": status.name,
            }
        )

    return result


@router.get("/{id}", response_model=ResponseTask)
def GetTask(id: int, session: SessionDep, username=Depends(auth_handler.auth_wrapper)):
#     if not CheckUser(creds.username, creds.password, session):
#         raise HTTPException(400, "Неверный логин или пароль!")

    user = session.exec(select(User).where(User.login == username)).first()
    check_task = session.exec(select(Task).where(Task.id == id, Task.user_id == user.id)).first()

    if check_task is None:
        raise HTTPException(404, "Задача не найдена")
    
    tasks = session.exec(
        select(Task, Priority, Status)
        .where(Task.id == id, Task.user_id == user.id)
        .join(Priority)
        .join(Status)
    ).all()


    result = ResponseTask

    for task, priority, status in tasks:
        result.id = task.id
        result.name = task.name
        result.description = task.description
        result.deadline = datetime.datetime.fromtimestamp(task.deadline).strftime(
            "%d.%m.%Y"
        )
        result.priority = priority.name
        result.status = status.name

    return result

@router.post("/")
def CreateTask(task: NewTask, session: SessionDep, username=Depends(auth_handler.auth_wrapper)):
#     if not CheckUser(creds.username, creds.password, session):
#         raise HTTPException(400, "Неверный логин или пароль!")
    
    priority = session.exec(select(Priority).where(Priority.name == task.priority.capitalize())).first()
    if priority is None:
        raise HTTPException(400, "Приоритет может быть только Low, Medium или High")
    
    status = session.exec(select(Status).where(Status.name == "In Progress")).first()
    user = session.exec(select(User).where(User.login == username)).first()

    res = Task(name=task.name,
                     description=task.description,
                     deadline=datetime.datetime.strptime(task.deadline, "%d.%m.%Y").timestamp(),
                     priority_id=priority.id,
                     status_id=status.id,
                     user_id=user.id)
    session.add(res)
    
    session.commit()
    
    return res

@router.patch("/")
def EditTask(task: EditTask, session: SessionDep, username=Depends(auth_handler.auth_wrapper)):
#     if not CheckUser(creds.username, creds.password, session):
#         raise HTTPException(400, "Неверный логин или пароль!")
    
    user = session.exec(select(User).where(User.login == username)).first()
    old_task = session.exec(select(Task).where(Task.id == task.id, Task.user_id == user.id)).first()

    if old_task is None:
        raise HTTPException(404, "Задача не найдена")

    if task.status is not None:
        status = session.exec(select(Status).where(Status.name == task.status.capitalize())).first()
        if status is None:
            raise HTTPException(400, "Статус может быть только In Progress, Cancelled или Completed")
        old_task.status_id = status.id

    if task.priority is not None:
        priority = session.exec(select(Priority).where(Priority.name == task.priority.capitalize())).first()
        if priority is None:
            raise HTTPException(400, "Приоритет может быть только Low, Medium или High")
        old_task.priority_id = priority.id
    
    if task.deadline is not None:
        old_task.deadline = datetime.datetime.strptime(task.deadline, "%d.%m.%Y").timestamp()
    
    if task.description is not None:
        old_task.description = task.description
    
    if task.name is not None:
        old_task.name = task.name

    session.add(old_task)
    session.commit()

    return {"message": "success"}

@router.delete("/")
def DeleteTask(id: int, session: SessionDep, username=Depends(auth_handler.auth_wrapper)):
#     if not CheckUser(creds.username, creds.password, session):
#         raise HTTPException(400, "Неверный логин или пароль!")
    
    user = session.exec(select(User).where(User.login == username)).first()
    task = session.exec(select(Task).where(Task.id == id, Task.user_id == user.id)).first()

    if task is None:
        raise HTTPException(404, "Задача не найдена")
    
    session.delete(task)
    session.commit()

    return {"message": "success"}