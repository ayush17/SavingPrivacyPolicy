import os
import json


def compile_json_files(input_folder, output_file):
    compiled_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        compiled_data.extend(data)
                    else:
                        compiled_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")

    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(compiled_data, f_out, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_folder = "./Data"
    output_file = "./compiled_data.json"
    compile_json_files(input_folder, output_file)
