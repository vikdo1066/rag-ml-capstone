from pydantic import BaseModel, Field

class Citation(BaseModel):
    chunk_id:    str
    document_id: str
    char_start:  int
    char_end:    int

class Answer(BaseModel):
    answer:    str | None        = Field(description="The answer text, or null if not in context.")
    citations: list[Citation]    = Field(default_factory=list)
    reason:    str | None        = Field(default=None, description="If answer is null, why.")
