import logging
import app.storage as storage 
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search/{collection}")
async def index(collection: str, q: str, limit: int = 10):
    logger.info(f"Search collection `{collection}` for `{q}`, limit: {limit}")
    return await storage.vector_search(collection, q, limit)