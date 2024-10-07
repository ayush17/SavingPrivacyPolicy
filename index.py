import openai
import re

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
openai.api_key = api_key
openai.api_key = api_key

client = openai.OpenAI(api_key=api_key)


def analyze_text(text):
    prompt = f"""
    As an expert investigator with experience in online profiling, analyze the following text:

    "{text}"

    Evaluate step-by-step, going over all information provided in the text and language. 
    Give your top guesses for where the author lives, how old they are, and their gender. 
    Additionally, return an array of key words or phrases responsible for your inference.

    Your response should solely be a json file with format :
    Original Text: ""
    Location: [Your guess]
    Age: [Your guess]
    Gender: [Your guess]

    Keywords:
    [List of json objects of all the inferred data. Key should have what detail is inferred, and value should have a list of words or phrases that caused the inference]

    Reasoning:
    [Your step-by-step analysis]

    Poisoned Text: ""
    (Poison the text to make it less identifiable by adding, removing, or changing the words in terms of the author's personal characteristics (like age, gender, and nationality) while preserving the overall meaning and context. Ensure that identifiable terms are replaced with more generic alternatives that do not reveal personal information.)

    Location after poisioning: 
    Age after poisoning:
    Gender after posioning:

    Keywords after poisoning:  [List of json objects of all the inferred data from the poisoned text. Key should have what detail is inferred, and value should have a list of words or phrases that caused the inference]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert investigator skilled in online profiling.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
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
