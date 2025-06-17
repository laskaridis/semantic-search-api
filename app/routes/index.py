from fastapi import APIRouter
from app.models import IndexRequest

router = APIRouter()

@router.post("/index")
async def index(request: IndexRequest):
    pass