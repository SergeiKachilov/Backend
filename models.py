from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship
from sqlmodel import Field as SqlField
import db
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from pydantic import Field as PydField

# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class Category(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str = SqlField(index=True)
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int | None = SqlField(default=None, primary_key=True)
    name: str
    description: str | None = SqlField(default=None)
    price: float
    category_id: int = SqlField(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")

class UpdateCategory(BaseModel):
    id: int | None = PydField(default=None, description="id изменяемого продукта")
    name: str | None = PydField(default=None)
    # products: list["Product"] = Relationship(back_populates="category")

class UpdateProduct(BaseModel):
    id: int | None = PydField(default=None, description="id изменяемого продукта")
    name: str | None = PydField(default=None)
    description: str | None = PydField(default=None)
    price: float | None = PydField(default=None)
    category_id: int | None= PydField(foreign_key="category.id", default=None)
    # category: Category = Relationship(back_populates="products")
