from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/task", tags=["Task"])

@router.get("/")
def task_index():
    return [{"title": "d"}]