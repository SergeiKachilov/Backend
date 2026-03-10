from pydantic import BaseModel, Field

class UserChoice(BaseModel):
    choice:str = Field("Камень")

class UserCreate(BaseModel):
    id:int|None
    username:str = Field(example="Ivanov123", min_length=3, max_length=50)
    email:str = Field(example="ivanov@mail.ru")
    password:str = Field(example="password123", min_length=8)
    full_name:str | None = Field(default=None)
    age:int | None = Field(None, ge=18, le=120)
    is_active:bool = Field(True)

class ItemCreate(BaseModel):
    name:str = Field(min_length=3, max_length=100)
    description:str | None = Field(max_length=1000)
    price:float = Field(ge=0.01, le=1000000)
    tax:float = Field(0, ge=0, le=100)
    tags:list[str] | None
    in_stock:bool = Field(True)
    quantity:int | None = Field(example=1, ge=0, le=1000)