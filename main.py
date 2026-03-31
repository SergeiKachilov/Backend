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

@app.post("/add_product")
def AddProduct(product: Product, session: SessionDep) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.delete("/delete_product")
def DeleteProduct(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"ok": True}

@app.patch("/update_product")
def UpdateProduct(product: UpdateProduct, session: SessionDep):
    old_product = session.get(Product, product.id)
    if not old_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name != None:
        old_product.name = product.name

    if product.description != None:
        old_product.description = product.description

    if product.price != None:
        old_product.price = product.price

    if product.category_id != None:
        old_product.category_id = product.category_id
    
    session.add(old_product)
    session.commit()
    session.refresh(old_product)
    return {"ok": True}

@app.get("/Category")
def GetCategories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Category]:
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

@app.get("/category/{category_id}")
def GetCategory(category_id: int, session: SessionDep) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    return category

@app.post("/add_category")
def AddCategory(category: Category, session: SessionDep) -> Category:
    # categories = select(Category).where(Category.name == category.name)
    # result = session.exec(categories)
    # if result:
    #     raise HTTPException(400, "category is already exist")
    session.commit()
    session.refresh(category)
    return category

@app.delete("/delete_category")
def DeleteCategory(category_id: int, session: SessionDep):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}

@app.patch("/update_category")
def UpdateCategory(category: UpdateCategory, session: SessionDep):
    old_category = session.get(Category, category.id)
    if not old_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.name != None:
        old_category.name = category.name
    
    session.add(old_category)
    session.commit()
    session.refresh(old_category)
    return {"ok": True}