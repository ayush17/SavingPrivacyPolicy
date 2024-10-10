import json

data = []
with open("synthpai.json", "r") as file:
    for line in file:
        if line.strip():
            data.append(json.loads(line))

authors_dict = {}

for entry in data:
    author = entry["author"]
    text = entry["text"]
    if author in authors_dict:
        authors_dict[author]["text"].append(text)
    else:
        authors_dict[author] = {
            "username": entry["username"],
            "profile": entry["profile"],
            "text": [text],
        }

output_data = []

for author, details in authors_dict.items():
    combined_text = ". ".join(details["text"])

    output_data.append(
        {
            "author": author,
            "username": details["username"],
            "profile": details["profile"],
            "text": combined_text,
        }
    )

with open("aggregated_authors.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print("Aggregation complete! Output saved to 'aggregated_authors.json'.")
