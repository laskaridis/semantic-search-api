from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
async def index(q: str, limit: int = 100):
    return {}