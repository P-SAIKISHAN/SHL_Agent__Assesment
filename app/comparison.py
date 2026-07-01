import re

from vectorstore.retriever import search
from app.llm import llm
from langchain_core.prompts import ChatPromptTemplate


comparison_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SHL Assessment expert.

Compare ONLY the two SHL assessments provided.

IMPORTANT:
- Always refer to the assessments using their actual names.
- Never call them "Assessment A" or "Assessment B".
- Use ONLY the supplied information.
- Do NOT invent facts.

Structure your comparison using these sections:

# Comparison of {name1} and {name2}

## 1. Purpose

## 2. What it measures

## 3. Typical use cases

## 4. Target audience

## 5. Strengths

## 6. Limitations

## 7. Recommendation
Explain when someone should choose one assessment over the other.
"""
        ),
        (
            "human",
            """
Assessment 1

Name:
{name1}

Description:
{desc1}

Categories:
{cat1}

Job Levels:
{level1}

Duration:
{duration1}

Languages:
{lang1}

Remote:
{remote1}

Adaptive:
{adaptive1}

--------------------------------------------

Assessment 2

Name:
{name2}

Description:
{desc2}

Categories:
{cat2}

Job Levels:
{level2}

Duration:
{duration2}

Languages:
{lang2}

Remote:
{remote2}

Adaptive:
{adaptive2}
"""
        )
    ]
)


def extract_assessments(query: str):
    """
    Extract two assessment names from a comparison query.
    """

    q = query.lower()

    for word in [
        "compare",
        "comparison",
        "between",
        "assessment",
        "assessments",
        "difference",
    ]:
        q = q.replace(word, "")

    parts = re.split(r"\bvs\b|\band\b|&|,", q)

    names = []

    for part in parts:
        part = part.strip()

        if part:
            names.append(part)

    return names[:2]


def compare_assessments(query: str):
    """
    Compare two SHL assessments.
    """

    names = extract_assessments(query)

    if len(names) < 2:
        return "Please specify two SHL assessments to compare."

    result1 = search(names[0], top_k=1)
    result2 = search(names[1], top_k=1)

    if not result1 or not result2:
        return "I couldn't find both SHL assessments."

    doc1 = result1[0]
    doc2 = result2[0]

    chain = comparison_prompt | llm

    response = chain.invoke(
        {
            "name1": doc1["name"],
            "desc1": doc1["description"],
            "cat1": ", ".join(doc1.get("categories", [])),
            "level1": ", ".join(doc1.get("job_levels", [])),
            "duration1": doc1.get("duration", ""),
            "lang1": ", ".join(doc1.get("languages", [])),
            "remote1": doc1.get("remote", ""),
            "adaptive1": doc1.get("adaptive", ""),

            "name2": doc2["name"],
            "desc2": doc2["description"],
            "cat2": ", ".join(doc2.get("categories", [])),
            "level2": ", ".join(doc2.get("job_levels", [])),
            "duration2": doc2.get("duration", ""),
            "lang2": ", ".join(doc2.get("languages", [])),
            "remote2": doc2.get("remote", ""),
            "adaptive2": doc2.get("adaptive", ""),
        }
    )

    return response.content