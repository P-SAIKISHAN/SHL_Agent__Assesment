import json
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

input_file = DATA_DIR / "shl_product_catalog.json"
clean_file = DATA_DIR / "cleaned_catalog.json"
search_file = DATA_DIR / "search_documents.json"
csv_file = DATA_DIR / "catalog.csv"

# -----------------------------
# Load original SHL catalog
# -----------------------------
with open(input_file, "r", encoding="utf-8") as f:
    catalog = json.load(f)

seen = set()
cleaned = []
search_docs = []

# -----------------------------
# Process every assessment
# -----------------------------
for item in catalog:

    entity_id = str(item.get("entity_id", "")).strip()

    if entity_id in seen:
        continue

    seen.add(entity_id)

    assessment = {
        "id": entity_id,
        "name": item.get("name", "").strip(),
        "url": item.get("link", "").strip(),
        "description": item.get("description", "").strip(),
        "job_levels": item.get("job_levels", []),
        "languages": item.get("languages", []),
        "duration": item.get("duration", "").strip(),
        "remote": item.get("remote", "").strip(),
        "adaptive": item.get("adaptive", "").strip(),
        "categories": item.get("keys", [])
    }

    cleaned.append(assessment)

    # ---------------------------------------
    # Build searchable text
    # ---------------------------------------
    search_text = f"""
Assessment Name: {assessment['name']}

Description:
{assessment['description']}

Categories:
{', '.join(assessment['categories'])}

Job Levels:
{', '.join(assessment['job_levels'])}

Languages:
{', '.join(assessment['languages'])}

Duration:
{assessment['duration']}

Remote Testing:
{assessment['remote']}

Adaptive:
{assessment['adaptive']}
"""

    # ---------------------------------------
    # Save ALL metadata for retrieval
    # ---------------------------------------
    search_docs.append({
        "id": assessment["id"],
        "name": assessment["name"],
        "url": assessment["url"],
        "description": assessment["description"],
        "job_levels": assessment["job_levels"],
        "languages": assessment["languages"],
        "duration": assessment["duration"],
        "remote": assessment["remote"],
        "adaptive": assessment["adaptive"],
        "categories": assessment["categories"],
        "text": search_text.strip()
    })

# -----------------------------
# Save cleaned catalog
# -----------------------------
with open(clean_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

# -----------------------------
# Save search documents
# -----------------------------
with open(search_file, "w", encoding="utf-8") as f:
    json.dump(search_docs, f, indent=4, ensure_ascii=False)

# -----------------------------
# Save CSV
# -----------------------------
pd.DataFrame(cleaned).to_csv(csv_file, index=False)

# -----------------------------
# Done
# -----------------------------
print("=" * 60)
print(f"Total Assessments : {len(cleaned)}")
print(f"Search Documents  : {len(search_docs)}")
print("Files Created Successfully")
print("=" * 60)