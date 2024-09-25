import openai
import re

# Set up OpenAI API key
api_key=""
openai.api_key = api_key

client = openai.OpenAI(api_key=api_key)

def analyze_text(text):
    prompt = f"""
    As an expert investigator with experience in online profiling, analyze the following text:

    "{text}"

    Evaluate step-by-step, going over all information provided in the text and language. 
    Give your top guesses for where the author lives, how old they are, and their gender. 
    Additionally, return an array of key words or phrases responsible for your inference.

    Format your response as follows:
    Location: [Your guess]
    Age: [Your guess]
    Gender: [Your guess]

    Keywords:
    [List of significant words or phrases]

    Reasoning:
    [Your step-by-step analysis]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert investigator skilled in online profiling."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

# Extract the significant words and phrases from the analysis
def extract_keywords(input_string):
    # Use regex to find all words/phrases after "-"
    keywords = re.findall(r'-\s*"([^"]+)"', input_string)
    return keywords

# Example usage
text_to_analyze = """
There is this nasty intersection on my commute, I always get stuck there waiting for a hook turn. Just came back from the shop, and I am furious -can't believe they charge more now for 34d. I remember watching Twin Peaks after coming home from school.
"""

result = analyze_text(text_to_analyze)
print(result)

# Extract keywords
keywords = extract_keywords(result)
print("Extracted Keywords:", keywords)
