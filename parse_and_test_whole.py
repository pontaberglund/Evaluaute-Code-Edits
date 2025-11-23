import json
import contextlib
from utils import test_logic, test_crash, test_class_extension


def parse_and_test_whole(file_path="model_responses.json"):
    # Read model_responses.json
    with open(file_path, "r") as f:
        data = json.load(f)

    # Filter responses for a specific edit type - whole
    whole_edit_responses = [
        entry for entry in data if entry['edit_type'] == 'whole']

    response = whole_edit_responses[0]['response']

    def extract_code_block(response):
        response = response.strip()
        code_block = None
        if response.startswith("```") and response.endswith("```"):
            code_block = "\n".join(response.split("\n")[1:-1])
        else:
            code_block = response
        return code_block

    logic_test_passed = 0
    logic_test_failed = 0
    crash_test_passed = 0
    crash_test_failed = 0
    class_extension_test_passed = 0
    class_extension_test_failed = 0

    # Keep stats for specific models
    models = [
        "x-ai/grok-4.1-fast:free",
        "kwaipilot/kat-coder-pro:free",
        "z-ai/glm-4.5-air:free",
        "google/gemma-3-4b-it:free",
        "google/gemma-3-12b-it:free",
        "nvidia/nemotron-nano-12b-v2-vl:free",
        "google/gemma-3-27b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "openai/gpt-oss-20b:free",
        "mistralai/mistral-small-3.1-24b-instruct:free"
    ]

    model_stats = {
        model: {
            "Logic Test": {"passed": 0, "failed": 0},
            "Crash Test": {"passed": 0, "failed": 0},
            "Class Extension Test": {"passed": 0, "failed": 0},
        }
        for model in models
    }

    failed_code_blocks = []

    for entry in whole_edit_responses:
        pre_code_block = entry["response"]
        model = entry["model"]
        code_block = extract_code_block(entry["response"])
        match entry["task"]:
            case "Logic Test":
                if test_logic(code_block):
                    logic_test_passed += 1
                    model_stats[model]["Logic Test"]["passed"] += 1
                else:
                    logic_test_failed += 1
                    model_stats[model]["Logic Test"]["failed"] += 1
                    failed_code_blocks.append((model, code_block))

            case "Crash Test":
                if test_crash(code_block):
                    crash_test_passed += 1
                    model_stats[model]["Crash Test"]["passed"] += 1
                else:
                    crash_test_failed += 1
                    model_stats[model]["Crash Test"]["failed"] += 1
                    failed_code_blocks.append((model, code_block))
            case "Class Extension Test":
                if test_class_extension(code_block):
                    class_extension_test_passed += 1
                    model_stats[model]["Class Extension Test"]["passed"] += 1
                else:
                    class_extension_test_failed += 1
                    model_stats[model]["Class Extension Test"]["failed"] += 1
                    failed_code_blocks.append((model, code_block))

    return {"logic_test_failed": logic_test_failed,
            "logic_test_passed": logic_test_passed,
            "crash_test_failed": crash_test_failed,
            "crash_test_passed": crash_test_passed,
            "class_extension_test_failed": class_extension_test_failed,
            "class_extension_test_passed": class_extension_test_passed,
            "model_stats": model_stats,
            "failed_code_blocks": failed_code_blocks}


with contextlib.redirect_stdout(None):
    results = parse_and_test_whole()
print("\nFailed Code Blocks:")
for model, code in results["failed_code_blocks"]:
    print("-----")
    print(f"Model: {model}")
    print(code)
    print("-----")

"""
print(
    f"Logic Test - Passed: {results['logic_test_passed']}, Failed: {results['logic_test_failed']}")
print(
    f"Crash Test - Passed: {results['crash_test_passed']}, Failed: {results['crash_test_failed']}")
print(
    f"Class Extension Test - Passed: {results['class_extension_test_passed']}, Failed: {results['class_extension_test_failed']}")

print("\nModel Specific Stats:")
for model, stats in results["model_stats"].items():
    print(f"\nModel: {model}")
    for test_type, result in stats.items():
        print(
            f"  {test_type} - Passed: {result['passed']}, Failed: {result['failed']}")
            
"""
