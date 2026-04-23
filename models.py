from sqlmodel import SQLModel, Relationship
from sqlmodel import Field as SqlField
from pydantic import BaseModel
from pydantic import Field as PydField
from datetime import datetime
from typing import List

# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class User(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    login: str = SqlField(unique=True, max_length=32)
    password: str = SqlField(max_length=16, min_length=8)
    
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)


class Status(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(unique=True)

class Task(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str
    description: str | None = SqlField(default=None)
    deadline: datetime | None = SqlField(default=None)
    status_id: int = SqlField(foreign_key="status.id")
    user_id: int = SqlField(foreign_key="user.id")

    status: Status = Relationship()
    user: User = Relationship(back_populates="tasks")

class RegUser(BaseModel):
    login: str
    password: str = PydField(min_length=8, pattern=r"[a-zA-Z]+[1-9]+|[1-9]+[a-zA-Z]+")

class NewTask(BaseModel):
    name: str
    description: str | None = PydField(default=None)
    deadline: str | None = PydField(default=None, pattern=r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$")
    priority: str | None = PydField(default="Low", description="Possible values: Low (default), Medium, High")

class EditTask(BaseModel):
    id: int
    name: str | None = PydField(default=None)
    description: str | None = PydField(default=None)
    deadline: str | None = PydField(default=None, pattern=r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$")
    priority: str | None = PydField(default=None)
    status: str | None = PydField(default=None)

class ResponseTask(BaseModel):
    id: int
    name: str
    description: str | None
    deadline: str | None
    priority: str
    status: str

# class Category(SQLModel, table=True):
#     id: int | None = SqlField(default=None, primary_key=True)
#     name: str
#     products: list["Product"] = Relationship(back_populates="category", cascade_delete=True)

# class Product(SQLModel, table=True):
#     id: int | None = SqlField(default=None, primary_key=True)
#     name: str
#     description: str | None = SqlField(default=None)
#     price: float
#     category_id: int = SqlField(foreign_key="category.id")
#     category: Category = Relationship(back_populates="products")

# class CreateProduct(BaseModel):
#     name: str
#     description: str | None = PydField(default=None)
#     price: float
#     category_id: int

# class CreateCategory(BaseModel):
#     name: str

# class UpdateCategory(BaseModel):
#     id: int = PydField(description="id изменяемой категории")
#     name: str | None = PydField(default=None)
#     # products: list["Product"] = Relationship(back_populates="category")

# class UpdateProduct(BaseModel):
#     id: int = PydField(description="id изменяемого продукта")
#     name: str | None = PydField(default=None)
#     description: str | None = PydField(default=None)
#     price: float | None = PydField(default=None)
#     category_id: int | None= PydField(foreign_key="category.id", default=None)
#     # category: Category = Relationship(back_populates="products")
