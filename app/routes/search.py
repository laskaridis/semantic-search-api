import logging
from app.models import SearchResult
import app.storage as storage
from fastapi import APIRouter, Query, HTTPException
from typing import Annotated, Union

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search/{collection}")
def search(
    collection: str,
    q: Annotated[str, Query(min_length=3, max_length=50)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10
) -> list[SearchResult]:
    logger.info(f"Search collection `{collection}` for `{q}`, limit: {limit}")
    try:
        return storage.vector_search(collection, q, limit)
    except storage.CollectionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))