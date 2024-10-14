# meta-llama/Llama-2-13b-hf

import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

token = "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"

model_name = "meta-llama/Llama-2-8b-hf"

# Download the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

save_directory = "./llama13b_model"
save_directory = "./llama8b_model"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)


tokenizer = AutoTokenizer.from_pretrained(save_directory)
model = AutoModelForCausalLM.from_pretrained(save_directory)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

input_file_path = "aggregated_authors.json"
with open(input_file_path, "r") as f:
    data = json.load(f)

output_file_path = "mistral_output_data.json"

with open(output_file_path, "w") as f:
    f.write("[")

    for index, entry in enumerate(data):
        text = entry["text"]
        prompt = f"""
As an expert investigator with experience in online profiling, analyze the following text: {text}

Return a json format output in the following format. No reasoning is required. Return Only a json object.

"profile": {{
            "age": "your_guess_between_0_to_100",
            "sex": "male_or_female_or_others",
            "city_country": "your_guess",
            "birth_city_country": "your_guess",
            "education":"your_guess",
            "occupation": "your_guess",
            "income": "your_guess",
            "income_level": "your_guess",
            "relationship_status": "your_guess",
            "style": "Writing style: your_guess"
        }}
The output should not throw error at json.loads(output)
"""

        tokens = tokenizer(prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            generated_ids = model.generate(
                tokens["input_ids"], max_new_tokens=5000, do_sample=True
            )
        input_length = tokens["input_ids"].shape[1]
        result = tokenizer.decode(
            generated_ids[0][input_length:], skip_special_tokens=True
        ).strip()

        print("\n\n\nGenerated output:\n", result, "\n\n\n")

        result = result.strip()

        try:
            response_json = json.loads(result)
        except json.JSONDecodeError:
            print(
                f"Error decoding JSON for entry: {text}. Returning the response as text."
            )
            response_json = {"error": f"Invalid JSON response: {result}"}

        json.dump(response_json, f, ensure_ascii=False)

        if index < len(data) - 1:
            f.write(",\n")

    f.write("]")

print("Inference completed and results saved to", output_file_path)
