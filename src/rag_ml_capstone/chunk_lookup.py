from google.cloud import storage
import dotenv
import json
from functools import lru_cache

dotenv.load_dotenv()

PROJECT_ID = dotenv.get_key(".env", "PROJECT_ID")

@lru_cache(maxsize=1)
def chunk_lookup() -> dict[str, dict]:
    client = storage.Client()
    blob = client.bucket(f"{PROJECT_ID}-embeddings").blob("chunks/chunks.jsonl")
    out: dict[str, dict] = {}
    with blob.open("r") as f:
        for line in f:
            chunk = json.loads(line)
            out[chunk["chunk_id"]] = chunk
    return out