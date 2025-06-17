from pydantic import BaseModel

class IndexRequest(BaseModel):
    id: str
    text: str

class SearchRequest(BaseModel):
    query: str
    max_items: int = 10


