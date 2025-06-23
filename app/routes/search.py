import logging
import app.storage as storage
from app.models import SearchResult
from fastapi import APIRouter, Query, Path, HTTPException
from typing import Annotated 
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()

class SearchParams(BaseModel):
    # disallow extra fields in query parameters
    model_config = { "extra": "forbid" }

    q: str = Field(..., min_length=3, max_length=50, title="Search query")
    limit: int = Field(10, ge=1, le=100, title="Results limit")

@router.get("/search/{collection}")
def search(
    collection: Annotated[str, Path(title="the collection name")],
    search_query: Annotated[SearchParams, Query()],
) -> list[SearchResult]:
    logger.info(f"Search collection `{collection}` for `{search_query.q}`, limit: {search_query.limit}")
    try:
        return storage.vector_search(collection, search_query.q, search_query.limit)
    except storage.CollectionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))