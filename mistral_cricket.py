import json
import csv
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

# Prepare the prompt with step-by-step reasoning and analysis
# Prepare the prompt with a clear request for CSV-like output
prompt = """
Generate a CSV-formatted text representing a ball-by-ball cricket match simulation with the following columns: 
"Over", "Ball", "Runs Scored", "Batsman Name", "Bowler Name", "Wickets", "Total Runs", 
"Total Wickets", "Balls Faced by Batsman", "Total Boundaries", "Extras". 

Please provide at least 50 overs of simulated match data in CSV format, including realistic values for runs scored, player names, and match events such as boundaries, wickets, and extras. 
Format the output as plain text, without any code or explanation. Each row should represent a delivery. Do the same for both teams, 50 overs each.
"""


# Tokenize the prompt
tokens = tokenizer(prompt, return_tensors="pt").to(device)

# Perform the inference with a low temperature (deterministic output)
with torch.no_grad():
    generated_ids = model.generate(
        tokens["input_ids"],
        max_new_tokens=50000,
        do_sample=True,
        temperature=0.1,
    )

# Decode the output and remove special tokens
input_length = tokens["input_ids"].shape[1]
result = tokenizer.decode(
    generated_ids[0][input_length:], skip_special_tokens=True
).strip()

# Display the generated output
print("\n\n\nGenerated output:\n", result, "\n\n\n")

# Try saving the output as CSV
output_csv_file_path = "mistral_output_data.csv"
output_txt_file_path = "mistral_output_data.txt"

try:
    with open(output_csv_file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write the header
        writer.writerow(
            [
                "Over",
                "Ball",
                "Runs Scored",
                "Batsman Name",
                "Bowler Name",
                "Wickets",
                "Total Runs",
                "Total Wickets",
                "Balls Faced by Batsman",
                "Total Boundaries",
                "Extras",
            ]
        )

        # Process the result line by line (assuming it's in a CSV-like format)
        for line in result.split("\n"):
            # Split the line by comma and strip whitespace
            row = [item.strip() for item in line.split(",")]
            if len(row) == 11:  # Ensure the correct number of columns
                # Write the row to the CSV file
                writer.writerow(row)
            else:
                raise ValueError("Row does not have the correct number of columns.")

    print("CSV file saved successfully.")

except Exception as e:
    print(f"Could not save as CSV. Error: {e}. Saving as text file instead.")

    # Save the output as a text file
    with open(output_txt_file_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Text file saved successfully to {output_txt_file_path}.")

print("Inference completed.")
