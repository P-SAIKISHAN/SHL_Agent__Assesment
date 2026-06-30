from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, MODEL_NAME
from app.prompts import SYSTEM_PROMPT

llm = ChatGroq(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """
User Query:
{query}

Available SHL Assessments:

{context}

Instructions:
- Recommend ONLY assessments from the provided context.
- Do NOT invent any assessment names.
- Briefly explain why each recommended assessment matches the user's request.
- If the context is insufficient, ask for clarification.
"""
        )
    ]
)


def generate_response(query: str, documents: list):
    """
    Generate a grounded recommendation using the retrieved SHL assessments.
    """

    if not documents:
        return "I couldn't find any relevant SHL assessments."

    context = ""

    for i, doc in enumerate(documents, start=1):
        context += f"""
Assessment {i}

Name:
{doc.get("name", "")}

Description:
{doc.get("description", "")}

Job Levels:
{", ".join(doc.get("job_levels", []))}

Categories:
{", ".join(doc.get("categories", []))}

Duration:
{doc.get("duration", "")}

Remote:
{doc.get("remote", "")}

Adaptive:
{doc.get("adaptive", "")}

URL:
{doc.get("url", "")}

----------------------------------------
"""

    try:
        chain = prompt | llm

        response = chain.invoke(
            {
                "query": query,
                "context": context
            }
        )

        return response.content

    except Exception as e:
        return f"LLM Error: {str(e)}"