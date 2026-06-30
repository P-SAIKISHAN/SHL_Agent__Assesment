BLOCKED = [
    "ignore previous instructions",
    "system prompt",
    "salary",
    "politics"
]

def is_blocked(query):
    q = query.lower()
    return any(word in q for word in BLOCKED)