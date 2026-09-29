import json

import dotenv
from google import genai
from google.cloud import storage

dotenv.load_dotenv()

PROJECT = dotenv.get_key(".env", "PROJECT_ID")
REGION = dotenv.get_key(".env", "REGION")

EMBEDDING_MODEL = dotenv.get_key(".env", "TEXT_EMBEDDING_MODEL")
EMBEDDING_DIMENSIONS = 768

client = genai.Client(project=PROJECT, vertexai=True, location=REGION)
storage_client = storage.Client(project=PROJECT)

CHUNK_BUCKET = f"{PROJECT}-embeddings"
src = storage_client.bucket(CHUNK_BUCKET).blob("chunks/chunks.jsonl")
dst = storage_client.bucket(CHUNK_BUCKET).blob("index/embeddings.json")

with src.open("r") as f_in, dst.open("w") as f_out:
    for line in f_in:
        chunk = json.loads(line)
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk["text"],
            config={
                "task_type": "RETRIEVAL_DOCUMENT",
                "output_dimensionality": EMBEDDING_DIMENSIONS,
            },
        )
        f_out.write(
            json.dumps(
                {
                    "id": chunk["chunk_id"],
                    "embedding": result.embeddings[0].values,
                    "restricts": [
                        {
                            "namespace": "document_id",
                            "allow_list": [chunk["document_id"]],
                        },
                    ],
                }
            )
            + "\n"
        )
