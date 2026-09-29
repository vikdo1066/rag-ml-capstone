import dotenv
from google import genai
from google.cloud import aiplatform

dotenv.load_dotenv()

PROJECT     = dotenv.get_key(".env", "PROJECT_ID")
REGION      = dotenv.get_key(".env", "REGION")
ENDPOINT_ID = dotenv.get_key(".env", "INDEX_ENDPOINT_ID")
DEPLOYED_ID = "rag_deployed_v1"
EMBED_MODEL = dotenv.get_key(".env", "TEXT_EMBEDDING_MODEL")

aiplatform.init(project=PROJECT, location=REGION)

client = genai.Client(vertexai=True, project=PROJECT, location=REGION)
qe = client.models.embed_content(
    model    = EMBED_MODEL,
    contents = "What is the alcohol policy on engagements?",
    config   = {"task_type": "RETRIEVAL_QUERY", "output_dimensionality": 768},
)

endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name = f"projects/{PROJECT}/locations/{REGION}/indexEndpoints/{ENDPOINT_ID}",
)
results = endpoint.find_neighbors(
    deployed_index_id = DEPLOYED_ID,
    queries           = [qe.embeddings[0].values],
    num_neighbors     = 5,
)
for r in results[0]:
    print(r.id, r.distance)