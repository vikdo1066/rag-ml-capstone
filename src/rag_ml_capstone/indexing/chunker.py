import hashlib
from .models import Chunk

CHUNK_TOKENS = 384
OVERLAP_TOKENS = 64
CHARS_PER_TOKEN = 4

def chunk_text(document_id: str, text: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    paragraphs = text.split("\n\n")
    buffer, char_start = [], 0
    for p in paragraphs:
        buffer.append(p)
        if sum(len(b) for b in buffer) > CHUNK_TOKENS * CHARS_PER_TOKEN:
            body = "\n\n".join(buffer)
            cid  = hashlib.sha256(
                f"{document_id}:{len(chunks)}".encode()
            ).hexdigest()[:16]
            chunks.append(Chunk(
                chunk_id    = cid,
                document_id = document_id,
                chunk_index = len(chunks),
                text        = body,
                char_start  = char_start,
                char_end    = char_start + len(body),
            ))
            char_start += len(body) - OVERLAP_TOKENS * CHARS_PER_TOKEN
            buffer = buffer[-1:]   # carry the last paragraph as overlap

    if buffer:
        body = "\n\n".join(buffer)
        chunks.append(Chunk(
            chunk_id    = hashlib.sha256(
                f"{document_id}:{len(chunks)}".encode()
            ).hexdigest()[:16],
            document_id = document_id,
            chunk_index = len(chunks),
            text        = body,
            char_start  = char_start,
            char_end    = char_start + len(body),
        ))
    return chunks
