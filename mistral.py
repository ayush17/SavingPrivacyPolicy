import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Hugging Face token (replace with an actual token if necessary)
token = "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"

# Define save directory for the model
save_directory = "./mistral_model"

# Load the tokenizer and model from the directory
tokenizer = AutoTokenizer.from_pretrained(save_directory, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(save_directory, use_auth_token=token)

# Set device to CUDA if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Load only one entry from the JSON file (e.g., the first entry)
input_file_path = "aggregated_authors.json"
with open(input_file_path, "r") as f:
    data = json.load(f)

# We will process only the first entry from the JSON file for testing
entry = data[0]
text = entry["text"]  # Extract the text from the current entry

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
        max_new_tokens=5000,
        do_sample=True,
        temperature=0.01,
    )

# Decode the output and remove special tokens
input_length = tokens["input_ids"].shape[1]
result = tokenizer.decode(
    generated_ids[0][input_length:], skip_special_tokens=True
).strip()

# Display the generated output
print("\n\n\nGenerated output:\n", result, "\n\n\n")

# Process the result and save it in JSON format
output_file_path = "mistral_output_data.json"
with open(output_file_path, "w") as f:
    result = result.strip()

    try:
        # Try parsing the generated result as JSON
        response_json = json.loads(result)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for entry: {text}. Returning the response as text.")
        response_json = {"error": f"Invalid JSON response: {result}"}

    # Save the response to the output file
    json.dump(response_json, f, ensure_ascii=False)

print("Inference completed and results saved to", output_file_path)
