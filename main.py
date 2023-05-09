import os
import json

if os.path.exists("messages.json"):
    os.remove("messages.json")

merged_data = {"participants": [], "messages": []}

# Keep track of whether the first file has been processed
first_file_processed = False

# Loop through all JSON files in the current directory
for filename in os.listdir("."):
    if filename.endswith(".json"):
        with open(filename, "r") as f:
            data = json.load(f)
            if "messages" in data:
                # Add messages to merged_data
                merged_data["messages"].extend(data["messages"])
            if not first_file_processed:
                # Add participants and title from the first file
                merged_data["participants"] = data.get("participants", [])
                merged_data["title"] = data.get("title", "")
                first_file_processed = True

# Sort messages based on timestamp_ms
merged_data["messages"].sort(key=lambda x: x["timestamp_ms"])

# Save merged data to a new file
with open("messages.json", "w") as f:
    json.dump(merged_data, f)
