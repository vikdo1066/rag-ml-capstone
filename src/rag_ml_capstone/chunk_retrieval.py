import dotenv
from dataclasses import dataclass
from google import genai
from google.cloud import aiplatform
from .chunk_lookup import chunk_lookup

dotenv.load_dotenv()

PROJECT_ID = dotenv.get_key(".env", "PROJECT_ID")
REGION = dotenv.get_key(".env", "REGION")
INDEX_ENDPOINT_ID = dotenv.get_key(".env", "INDEX_ENDPOINT_ID")

EMBED_MODEL       = dotenv.get_key(".env", "TEXT_EMBEDDING_MODEL")
EMBED_DIMS        = 768
DEPLOYED_INDEX_ID = "rag_deployed_v1" #dotenv.get_key(".env", "RAG_INDEX_ID")

aiplatform.init(project=PROJECT_ID, location=REGION)
INDEX_ENDPOINT=aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=f"projects/1090787004089/locations/{REGION}/indexEndpoints/{INDEX_ENDPOINT_ID}")

genai = genai.Client(vertexai=True, project=PROJECT_ID, location=REGION)

@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    text: str
    score: float
    char_start: int
    char_end: int

def retrieve_chunk(query: str, k: int = 5) -> list[RetrievedChunk]:
    if not query.strip():
        return []

    query_embedding = genai.models.embed_content(
        model=EMBED_MODEL,
        contents=query,
        config={
            "output_dimensionality": EMBED_DIMS,
            "task_type": "RETRIEVAL_QUERY"})
            
    raw = INDEX_ENDPOINT.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID, 
        queries=[query_embedding.embeddings[0].values],
        num_neighbors=k)

    if not raw or not raw[0]:
        return []

    lookup = chunk_lookup()
    out: list[RetrievedChunk] = []
    for neighbor in raw[0]:
        chunk = lookup.get(neighbor.id)
        if chunk is None:
            continue
        else:
            out.append(RetrievedChunk(
                chunk_id=chunk["chunk_id"],
                document_id=chunk["document_id"],
                text=chunk["text"],
                score=neighbor.distance,
                char_start  = chunk["char_start"],
                char_end    = chunk["char_end"],
            ))
    return out
