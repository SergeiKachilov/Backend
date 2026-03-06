from fastapi import FastAPI, HTTPException
from enum import Enum

import random
import pyd

app = FastAPI()

choices = ["Камень", "Ножницы", "Бумага"]

winCombinations = {
    "Камень": "Ножницы",
    "Ножницы": "Бумага",
    "Бумага": "Камень"
}

@app.post("/rps")
def RPS(userChoice:pyd.UserChoice):
    if userChoice.choice.capitalize() not in choices:
        raise HTTPException(400, "Недопустимое значение")
    
    compChoice = random.choice(choices)

    if userChoice.choice.capitalize() == compChoice:
        return {
            "user_choice":userChoice.choice.capitalize(),
            "computer_choice":compChoice,
            "result": "Ничья"
        }
    
    if winCombinations[userChoice.choice.capitalize()] == compChoice:
        return {
            "user_choice":userChoice.choice.capitalize(),
            "computer_choice":compChoice,
            "result": "Победа"
        }
    
    return {
            "user_choice":userChoice.choice.capitalize(),
            "computer_choice":compChoice,
            "result": "Поражение"
        }
