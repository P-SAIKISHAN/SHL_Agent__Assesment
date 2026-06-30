from app.guardrails import is_blocked


def classify_intent(query: str) -> str:
    q = query.lower().strip()

    # Guardrails
    if is_blocked(q):
        return "blocked"

    # Compare
    if "compare" in q or "difference" in q:
        return "compare"

    # Refinement
    if any(word in q for word in ["actually", "instead", "also", "add", "remove"]):
        return "refine"

    # Clarification
    vague_queries = {
        "assessment",
        "need assessment",
        "recommend assessment",
        "test",
        "need test",
        "help me hire",
        "suggest assessment",
    }

    if q in vague_queries:
        return "clarify"

    # Default
    return "recommend"