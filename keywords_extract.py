import json
import os


def extract_author_and_keywords(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        compiled_data = json.load(f)

    extracted_data = []

    for item in compiled_data:
        author = item.get("author", "Unknown Author")
        keywords = item.get("keywords", "No keywords")

        extracted_data.append({"author": author, "keywords": keywords})

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(extracted_data, f_out, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file = "./compiled_data.json"
    output_file = "./author_keywords.json"
    extract_author_and_keywords(input_file, output_file)
