from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship
import db
from fastapi import Depends, FastAPI, HTTPException, Query

# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = Field(default=None)
    price: float
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
