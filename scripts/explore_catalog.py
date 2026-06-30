import json
from pprint import pprint

with open("data/shl_product_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total Assessments:", len(data))

print("\nType:", type(data))

print("\nKeys in first record:")
print(data[0].keys())

print("\nFirst Assessment:")
pprint(data[0])