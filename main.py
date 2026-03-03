from fastapi import FastAPI, Path, Query
from enum import Enum
import random
from math import sqrt

app = FastAPI()

class Units(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"

@app.get("/about")
def About():
    return {
        "FullName": "Качилов Сергей Евгеньевич",
        "Group": "T-333901",
        "course": 3,
        "university": "НТИ УРФУ"
    }

@app.get("/rnd")
def Rnd():
    return {"rnd": random.randint(0, 1000)}

@app.post("/t_square")
def T_Square(a:float = Query(gt=0), b:float = Query(gt=0), c:float = Query(gt=0)):
    if (((a + b) > c) & ((a + c) > b) & ((b + c) > a)):
        p = a + b + c
        s = sqrt(p/2*(p/2-a)*(p/2-b)*(p/2-c))
        return {
            "perimeter": p,
            "square": s
        }
    return {
        "error": "Треугольник не существует"
    }

@app.get("/convert/{from_unit}/{to_unit}/{value}")
def Convert(from_unit:Units, to_unit:Units, value:float):
    if from_unit in Units.celsius:
        if to_unit in Units.fahrenheit:
            t = value * 9 / 5 + 32
            return {
                "initial": str(value) + " C",
                "result": str(t) + " F"
                }
        elif to_unit in Units.celsius:
            return {
                "initial": str(value) + " C",
                "result": str(value) + " C"
                }
    elif from_unit in Units.fahrenheit:
        if to_unit in Units.fahrenheit:
            return {
                "initial": str(value) + " F",
                "result": str(value) + " F"
                }
        elif to_unit in Units.celsius:
            t = (value - 32)  * 5 / 9
            return {
                "initial": str(value) + " F",
                "result": str(t) + " C"
                }
