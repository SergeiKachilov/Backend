from pydantic import BaseModel, Field

class UserChoice(BaseModel):
    choice:str = Field("Камень")