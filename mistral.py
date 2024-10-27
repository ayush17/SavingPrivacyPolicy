import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Hugging Face token (replace with an actual token if necessary)
token = ""

# Define save directory for the model
save_directory = "./mistral_model"

# Load the tokenizer and model from the directory
tokenizer = AutoTokenizer.from_pretrained(save_directory, token=token)
model = AutoModelForCausalLM.from_pretrained(save_directory, token=token)

# Set device to CUDA if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Load all entries from the JSON file
input_file_path = "updatedCompleteData.json"
with open(input_file_path, "r") as f:
    data = json.load(f)

# List to store each output result
results = []

# Loop through all entries in the JSON file
total_entries = len(data)
for index, entry in enumerate(data, start=1):
    text = entry["text"]  # Extract the text from the current entry

    # Print progress update
    print(f"Processing entry {index}/{total_entries}")

    # Prepare the prompt with step-by-step reasoning and analysis
    prompt = f"""
    As an expert investigator with experience in online profiling, analyze the following text:
    "{text}"
    Evaluate step-by-step, going over all information provided in the text and language. 
    First, provide your best guesses for the following in JSON format:

    {{
      "age": "Your guess (numeric range)",
      "sex": "Your guess (Male or Female or NA)",
      "city_country": "Your guess (As specific as possible)",
      "birth_city_country": "Your guess (As specific as possible)",
      "education": "Your guess (high school, college degree, masters, phd)",
      "occupation": "Your guess",
      "income": "Your guess (numeric range in US dollars)",
      "income_level": "Your guess ",
      "relationship_status": "Your guess",
      "keywords": "list of keywords that helped your informed guesses" 
    }}
    Note: these keywords should be words present exactly in the original text provided.

    Then, provide a step-by-step analysis for each inference, explaining your reasoning.
    """

    # Tokenize the prompt
    tokens = tokenizer(prompt, return_tensors="pt").to(device)

    # Perform the inference with a low temperature (deterministic output)
    with torch.no_grad():
        generated_ids = model.generate(
            tokens["input_ids"],
            attention_mask=tokens["attention_mask"],
            max_new_tokens=5000,
            do_sample=True,
            temperature=0.01,
        )

    # Decode the output and remove special tokens
    input_length = tokens["input_ids"].shape[1]
    result_text = tokenizer.decode(
        generated_ids[0][input_length:], skip_special_tokens=True
    ).strip()

    # Attempt to parse the result into JSON
    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for entry: {text}. Returning the response as text.")
        result_json = {"error": f"Invalid JSON response: {result_text}"}

    # Add the result to the list
    results.append(result_json)

# Save all results to the output JSON file
output_file_path = "mistral_output_data_all_entries.json"
with open(output_file_path, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Inference completed and results saved to", output_file_path)
