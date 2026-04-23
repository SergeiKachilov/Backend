from fastapi import FastAPI, UploadFile
import routers
import shutil
from uuid import uuid4

app = FastAPI()
app.include_router(routers.task_router)

@app.post("/load_img")
def Load_img(file: UploadFile):
    file_location = f"upload/{uuid4()}.{file.filename.split('.')[-1]}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    return {"src": file_location, "old_name":file.filename}