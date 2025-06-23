import logging
import app.storage as storage
from fastapi import APIRouter, Response

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/collections/{name}")
async def create_collection(name: str):
    if storage.create_collection(name):
        return Response(status_code=201)
    else:
        logger.error(f"Collection '{name}' was not created.")
        return Response(status_code=200)

@router.delete("/collections/{name}")
async def delete_collection(name: str):
    if storage.delete_collection(name):
        return Response(status_code=204)
    else:
        return Response(status_code=404)

@router.get("/collections")
async def list_collections():
    collections = storage.list_collections()
    return {"collections": collections}


@router.get("/collections/{name}")
async def show_collection(name: str):
    collection = storage.show_collection(name)
    if collection:
        return collection
    else:
        return Response(status_code=404)