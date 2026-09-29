from rag_ml_capstone.answer import answer

for q in [
    "Can I claim alcohol on a client dinner?",
    "What is the cap on travel without manager approval?",
    "What's a good recipe for chocolate cake?",
]:
    a = answer(q)
    print(f"\nQ: {q}")
    print(f"  answer:    {a.answer}")
    print(f"  reason:    {a.reason}")
    print(f"  citations: {[c.chunk_id for c in a.citations]}")