from fastapi import FastAPI
from classes import CreateProduct
from typing import Annotated
from models import *
from db import create_db_and_tables, SessionDep

from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select

app = FastAPI()


count = 0
data = []


# @app.get("/main")
# def effg():
#     global count
#     count += 1
#     return {"hello": count}


# @app.post("/addproduct")
# def add_product(product: CreateProduct):
#     data.append(product)
#     return data


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()



# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}

@app.get("/product")
def GetProducts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Product]:
    heroes = session.exec(select(Product).offset(offset).limit(limit)).all()
    return heroes

@app.get("/product/{product_id}")
def GetProduct(product_id: int, session: SessionDep) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@app.post("/add_product/")
def AddProduct(product: Product, session: SessionDep) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

