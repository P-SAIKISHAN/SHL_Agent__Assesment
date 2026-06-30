from app.planner import classify_intent
from app.llm import generate_response
from vectorstore.retriever import search


def handle_messages(messages):
    """
    Main orchestration function using conversation history.
    """

    # -----------------------------------------------------
    # Collect all user messages
    # -----------------------------------------------------
    user_messages = []

    latest_query = ""

    for msg in messages:
        if msg.role == "user":
            user_messages.append(msg.content)
            latest_query = msg.content

    # Combined query for retrieval
    search_query = " ".join(user_messages)

    # -----------------------------------------------------
    # Detect intent
    # -----------------------------------------------------
    intent = classify_intent(latest_query)

    # -----------------------------------------------------
    # Blocked Queries
    # -----------------------------------------------------
    if intent == "blocked":
        return {
            "reply": "Sorry, I can only help with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------------------------------
    # Clarification
    # -----------------------------------------------------
    if intent == "clarify":
        return {
            "reply": (
                "I'd be happy to help recommend SHL assessments.\n\n"
                "Please tell me:\n"
                "• Job title\n"
                "• Experience level\n"
                "• Required technical skills\n"
                "• Or simply paste the Job Description."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------------------------
    # Recommendation
    # -----------------------------------------------------
    if intent == "recommend":

        results = search(search_query, top_k=5)

        if not results:
            return {
                "reply": "Sorry, I couldn't find any relevant SHL assessments.",
                "recommendations": [],
                "end_of_conversation": False
            }

        recommendations = []

        for item in results:
            recommendations.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": ", ".join(item.get("categories", []))
            })

        reply = generate_response(search_query, results)

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # -----------------------------------------------------
    # Refinement
    # -----------------------------------------------------
    if intent == "refine":

        # Reuse all previous user requests
        results = search(search_query, top_k=5)

        if not results:
            return {
                "reply": "I couldn't find refined SHL assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": False
            }

        recommendations = []

        for item in results:
            recommendations.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": ", ".join(item.get("categories", []))
            })

        reply = generate_response(search_query, results)

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # -----------------------------------------------------
    # Comparison (Next Step)
    # -----------------------------------------------------
    if intent == "compare":
        return {
            "reply": "Comparison feature is under development.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------
    return {
        "reply": "Sorry, I couldn't understand your request.",
        "recommendations": [],
        "end_of_conversation": False
    }