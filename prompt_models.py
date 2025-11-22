from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time
from tqdm import tqdm

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

"""
First we define a list of models to try out.
"""

models_to_try = [
    "x-ai/grok-4.1-fast:free",
    "kwaipilot/kat-coder-pro:free",
    "z-ai/glm-4.5-air:free",
    "google/gemma-3-4b-it:free",
    "google/gemma-3-12b-it:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "openai/gpt-oss-20b:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]

"""
Next, we define the edit types we want to test on each model.
"""

edit_types = [
    "whole",
    "diff",
    "udiff"
]
edit_types_prompts = [
    "You should return the entire corrected code without any additional explanations or comments.",

    "You should return the edits only in the form of a diff. Return a series of search/replace blocks that can be applied to the original code to get the corrected code. For the answer, use the format\n<<<<<<< SEARCH\n[Block of code to be replaced]\n=======\n[Block of code to use instead]\nREPLACE>>>>>>>.\nAn example is shown below:\n\n<<<<<<< SEARCH\nfrom flask import Flask\n=======\nimport math\nfrom flask import Flask\nREPLACE>>>>>>>\n\nOnly include the search/replace blocks without any additional explanations or comments.",

    "You should return the edits in the UDIFF format. Do not output the entire file. Only output the parts of the file that have changed, along with the necessary context to locate the change. Use @@ ... @@ to separate distinct blocks of changes. Do not attempt to calculate line numbers (e.g., do not use @@ -12,4 +12,5 @@). simply use @@ ... @@. Start lines with - to denote code removal. Start lines with + to denote code addition. Provide 1-2 lines of unchanged context before and after the change to ensure uniqueness, but do not use a prefix for context lines.\n\nAn example is shown below:\n\n@@ ... @@\ndef calculate_total(prices):\n-    return sum(prices)\n+    return sum(prices) * 1.2\n\nOnly include the UDIFF output without any additional explanations or comments."
]

"""
Build the prompts
"""

crash_test_prompts = [
    f"{open('prompts/crash_test.txt').read()}\n\n{edit_type}"
    for edit_type in edit_types_prompts
]

class_extension_prompts = [
    f"{open('prompts/class_extension_test.txt').read()}\n\n{edit_type}"
    for edit_type in edit_types_prompts
]

logic_test_prompts = [
    f"{open('prompts/logic_test.txt').read()}\n\n{edit_type}"
    for edit_type in edit_types_prompts
]

"""
Print the prompts for verification"""

print("Crash Test Prompts:")
for prompt in crash_test_prompts:
    print("-----")
    print(prompt)
    print("-----")

print("Class Extension Test Prompts:")
for prompt in class_extension_prompts:
    print("-----")
    print(prompt)
    print("-----")

print("Logic Test Prompts:")
for prompt in logic_test_prompts:
    print("-----")
    print(prompt)
    print("-----")

"""
Prompt the models and collect responses in a structured way
"""

output_data = []
for model in tqdm(models_to_try, desc="Models"):
    for prompt_set, prompt_set_name in [
        (crash_test_prompts, "Crash Test"),
        (class_extension_prompts, "Class Extension Test"),
        (logic_test_prompts, "Logic Test")
    ]:
        for edit_type_index, prompt in enumerate(prompt_set):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    extra_body={"reasoning": {"enabled": True}}
                )
                # Check for valid response
                if response:
                    response_dict = response.model_dump()
                    content = response.choices[0].message.content
                    output_data.append({
                        "model": model,
                        "edit_type": edit_types[edit_type_index],
                        "task": prompt_set_name,
                        "prompt_text": prompt,
                        "response": content,
                        "response_dict": response_dict,
                        "status": "success"
                    })
                else:
                    print(
                        f"No valid response for this model and prompt. {model}, {prompt_set_name}, {edit_types[edit_type_index]}")
                    output_data.append({
                        "model": model,
                        "edit_type": edit_types[edit_type_index],
                        "task": prompt_set_name,
                        "prompt_text": prompt,
                        "response": content,
                        "response_dict": response_dict,
                        "status": "error - no response"
                    })
            except Exception as e:
                print(
                    f"Exception for model {model} with prompt set {prompt_set_name} and edit type {edit_types[edit_type_index]}: {e}")
                output_data.append({
                    "model": model,
                    "edit_type": edit_types[edit_type_index],
                    "task": prompt_set_name,
                    "prompt_text": prompt,
                    "response": "",
                    "response_dict": {"error": str(e)},
                    "status": "error"
                })

            time.sleep(15)  # To avoid hitting rate limits

# Save to JSON
with open("model_responses_mistral.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Responses saved to model_responses_mistral.json")
