# tools/generate_corpus.py
import pathlib

DOCS = {
    "expense-policy.md":       "...",  # one ~500-word body each
    "leave-policy.md":         "...",
    "remote-work-policy.md":   "...",
    "code-of-conduct.md":      "...",
    "data-handling-policy.md": "...",
}

OUT = pathlib.Path("local/corpus")
OUT.mkdir(parents=True, exist_ok=True)
for name, body in DOCS.items():
    (OUT / name).write_text(body.strip())