import json
from google.genai import types
from .chunk_retrieval import genai, retrieve_chunk
from .answer_schema import Answer


SYSTEM_PROMPT = """\
You are a Datatonic policy assistant. Answer questions ONLY from
the supplied policy excerpts. For every factual claim in your
answer, cite the chunk it came from using the chunk_id.

If the supplied excerpts do not contain the answer, set `answer`
to null and provide `reason: "not_in_context"`. Do NOT use prior
knowledge or invent details. Use only the chunk_id values from
the excerpts.

Excerpts are formatted as:
  <chunk id="abc123" document="expense-policy.md">
    ...chunk text...
  </chunk>

Respond strictly in the JSON schema provided.
"""

def build_user_prompt(query: str, chunks) -> str:
    parts = ["Excerpts:"]
    for c in chunks:
        parts.append(
            f'<chunk id="{c.chunk_id}" document="{c.document_id}">\n'
            f'{c.text}\n'
            f'</chunk>'
        )
    parts.append(f"\nQuestion: {query}")
    return "\n\n".join(parts)

# Flash is the RAG default — retrieval does the grounding lift, so
# the generation model can be smaller, faster, and cheaper.
# Engagements with high-stakes corpora (regulated, legal, medical,
# expert-knowledge) where the wrong-answer cost is high should
# flip to Pro.
ANSWER_MODEL = "gemini-2.5-flash"

def answer(query: str, k: int = 5) -> Answer:
    chunks = retrieve_chunk(query, k=k)
    if not chunks:
        return Answer(answer=None, reason="no_retrieval_results")

    user_prompt = build_user_prompt(query, chunks)

    response = genai.models.generate_content(
        model    = ANSWER_MODEL,
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)])],
        config   = types.GenerateContentConfig(
            system_instruction = SYSTEM_PROMPT,
            temperature        = 0.1,
            # 2.5 Flash spends part of this budget on thinking tokens.
            max_output_tokens  = 4096,
            response_mime_type = "application/json",
            response_schema    = Answer,
            # thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    if response.parsed is not None:
        return response.parsed
    return Answer.model_validate(json.loads(response.text))