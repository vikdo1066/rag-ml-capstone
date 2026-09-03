from pydantic import BaseModel, Field

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    char_start: int
    char_end: int
    metadata: dict = Field(default_factory=dict)