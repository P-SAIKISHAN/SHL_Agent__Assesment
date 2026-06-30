import json
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

input_file = DATA_DIR / "shl_product_catalog.json"
clean_file = DATA_DIR / "cleaned_catalog.json"
search_file = DATA_DIR / "search_documents.json"
csv_file = DATA_DIR / "catalog.csv"

with open(input_file, "r", encoding="utf-8") as f:
    catalog = json.load(f)

seen = set()
cleaned = []
search_docs = []

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

    search_docs.append({
        "id": assessment["id"],
        "name": assessment["name"],
        "url": assessment["url"],
        "text": search_text.strip()
    })

with open(clean_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4)

with open(search_file, "w", encoding="utf-8") as f:
    json.dump(search_docs, f, indent=4)

pd.DataFrame(cleaned).to_csv(csv_file, index=False)

print("=" * 50)
print(f"Total Assessments : {len(cleaned)}")
print(f"Search Documents  : {len(search_docs)}")
print("Files Created Successfully")
print("=" * 50)