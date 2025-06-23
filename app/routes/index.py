import logging
from fastapi import APIRouter, Response, status
from app.models import IndexRequest
from app.storage import vector_find, vector_index

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/index/{collection}")
async def index(collection: str, request: IndexRequest):
    if not vector_find(collection, request.id):
        vector_index(collection, request)
    return Response(status_code=201)