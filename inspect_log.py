import json

with open("data/user_activity_log.json") as f:
    data = json.load(f)

# Print the first record
print("✅ First record:", data[0])
print("✅ Keys:", list(data[0].keys()))
