import json

data = []
with open("synthpai.json", "r") as file:
    for line in file:
        if line.strip():  # Skip empty lines
            data.append(json.loads(line))

# Dictionary to hold unique authors and their aggregated data
authors_dict = {}

# Process each entry in the dataset
for entry in data:
    author = entry["author"]
    text = entry["text"]

    # If the author is already in the dictionary, concatenate the text
    if author in authors_dict:
        authors_dict[author]["text"].append(text)
    else:
        # If the author is not present, add them to the dictionary
        authors_dict[author] = {
            "username": entry["username"],
            "profile": entry["profile"],
            "text": [text],
        }

# Prepare the final output
output_data = []

# Iterate through the aggregated data to format the output
for author, details in authors_dict.items():
    # Concatenate all text fields into a single string separated by a full stop
    combined_text = ". ".join(details["text"])

    output_data.append(
        {
            "author": author,
            "username": details["username"],
            "profile": details["profile"],
            "text": combined_text,
        }
    )

# Write the output to a new JSON file
with open("aggregated_authors.json", "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print("Aggregation complete! Output saved to 'aggregated_authors.json'.")
