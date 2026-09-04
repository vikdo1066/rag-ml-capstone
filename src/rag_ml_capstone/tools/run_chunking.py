import dotenv
from google.cloud import storage
from rag_ml_capstone.indexing.chunker import chunk_text

dotenv.load_dotenv()

PROJECT = dotenv.get_key(".env", "PROJECT_ID")

client = storage.Client(project=PROJECT)
raw_bucket = client.bucket(f"{PROJECT}-raw-docs")
embedding_bucket = client.bucket(f"{PROJECT}-embeddings")

with embedding_bucket.blob("chunks/chunks.jsonl").open("w") as out:
    for blob in raw_bucket.list_blobs(prefix="policies/"):
        text = blob.download_as_text()
        chunks = chunk_text(blob.name, text)
        for chunk in chunks:
            out.write(chunk.model_dump_json() + "\n")