from pydantic import BaseModel, Field

class IndexRequest(BaseModel):
    id: str = Field(..., description="External ID of the item to index")
    text: str = Field(..., description="Text content of the item to index")

class SearchResult(BaseModel):
    id: str = Field(..., description="External ID of the item found")
    text: str = Field(..., description="Text content of the item found")
    score: float = Field(..., description="Relevance score of the item found")