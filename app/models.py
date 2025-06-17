from pydantic import BaseModel, Field

class IndexRequest(BaseModel):
    id: str = Field(..., description="External ID of the item to index")
    text: str = Field(..., description="Text content of the item to index")

