import json

with open("data/shl_product_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(len(data))

print("\nFirst record:\n")
print(data[0])