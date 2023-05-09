import json

# Define the mapping of characters to replace
char_map = {"Ä": "ć", "Ä": "č", "Å ": "Š", "Å¡": "š", "Å½": "Ž", "Å¾": "ž", "\u00e2\u0080\u0099": "'"}

# Load the JSON file
with open("messages.json", "r") as file:
    data = json.load(file)

# Define a function to recursively search for and replace characters in the data
def replace_chars(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_chars(value)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            data[i] = replace_chars(value)
    elif isinstance(data, str):
        for char, replacement in char_map.items():
            data = data.replace(char, str(replacement))
    return data

# Replace the characters in the data
data = replace_chars(data)

# Save the modified data back to the JSON file
with open("messages.json", "w") as file:
    json.dump(data, file)
