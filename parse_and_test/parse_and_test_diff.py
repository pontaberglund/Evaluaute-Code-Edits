import json
import contextlib
import re

from utils import test_logic, test_crash, test_class_extension, LOGIC_TEST_CODE_SNIPPET, CRASH_TEST_CODE_SNIPPET, CLASS_EXTENSION_TEST_CODE_SNIPPET


def parse_and_test_diff(file_path="model_responses.json"):
    # Read model_responses.json
    with open("model_responses.json", "r") as f:
        data = json.load(f)

    # Filter responses for a specific edit type - diff
    diff_edit_responses = [
        entry for entry in data if entry['edit_type'] == 'diff']

    def extract_code_block(response, task):
        response = response
        if response.startswith("```") and response.endswith("```"):
            response = "\n".join(response.split("\n")[1:-1])

        # Extract SEARCH/REPLACE sections
        pattern = r"<{3,}\s*SEARCH\s*\n(.*?)\n\s*={3,}\s*\n(.*?)\n\s*(?:>{3,}\s*REPLACE|REPLACE\s*>{3,}|>{3,})"
        matches = re.findall(pattern, response, re.DOTALL)

        code_block = None
        if task == "Logic Test":
            code_block = LOGIC_TEST_CODE_SNIPPET
        elif task == "Crash Test":
            code_block = CRASH_TEST_CODE_SNIPPET
        elif task == "Class Extension Test":
            code_block = CLASS_EXTENSION_TEST_CODE_SNIPPET
        for search, replace in matches:
            # If exact match, do direct replace
            if search in code_block:
                code_block = code_block.replace(search, replace)
            # Else do line by line match, with normalization
            else:
                search_lines = [line.strip() for line in search.splitlines()]
                code_lines = code_block.splitlines()

                for i in range(len(code_lines) - len(search_lines) + 1):
                    chunk = code_lines[i:i + len(search_lines)]
                    chunk_stripped = [line.strip() for line in chunk]

                    if chunk_stripped == search_lines:
                        indent = ""
                        for line in chunk:
                            if line.strip():
                                indent = line[:line.find(line.strip())]
                                break
                        replace_lines = replace.splitlines()
                        new_replace_lines = [
                            indent + line for line in replace_lines]
                        code_lines[i:i + len(search_lines)] = new_replace_lines
                        code_block = "\n".join(code_lines)
                        break

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

    for entry in diff_edit_responses:
        pre_code_block = entry["response"]
        model = entry["model"]
        match entry["task"]:
            case "Logic Test":
                code_block = extract_code_block(
                    entry["response"], "Logic Test")

                code_block += ("\ndata=[10,2,5]\nresult=calculate_median(data)")
                if test_logic(code_block):
                    logic_test_passed += 1
                    model_stats[model]["Logic Test"]["passed"] += 1
                else:
                    logic_test_failed += 1
                    model_stats[model]["Logic Test"]["failed"] += 1
                    failed_code_blocks.append((pre_code_block, code_block))

            case "Crash Test":
                code_block = extract_code_block(
                    entry["response"], "Crash Test")

                code_block += ("\nids=[1,2,3,4,5]\nprocess_user_ids(ids)")

                if test_crash(code_block):
                    crash_test_passed += 1
                    model_stats[model]["Crash Test"]["passed"] += 1
                else:
                    crash_test_failed += 1
                    model_stats[model]["Crash Test"]["failed"] += 1
                    failed_code_blocks.append((pre_code_block, code_block))

            case "Class Extension Test":
                code_block = extract_code_block(
                    entry["response"], "Class Extension Test")

                code_block += ("\nstore=InventoryManager()\nstore.add_stock('apple',10)\nstore.remove_stock('apple',4)\ncurrent_stock=store.check_stock('apple')")

                if test_class_extension(code_block):
                    class_extension_test_passed += 1
                    model_stats[model]["Class Extension Test"]["passed"] += 1
                else:
                    class_extension_test_failed += 1
                    model_stats[model]["Class Extension Test"]["failed"] += 1
                    failed_code_blocks.append((pre_code_block, code_block))

    return {"logic_test_failed": logic_test_failed,
            "logic_test_passed": logic_test_passed,
            "crash_test_failed": crash_test_failed,
            "crash_test_passed": crash_test_passed,
            "class_extension_test_failed": class_extension_test_failed,
            "class_extension_test_passed": class_extension_test_passed,
            "model_stats": model_stats,
            "failed_code_blocks": failed_code_blocks}


with contextlib.redirect_stdout(None):
    results = parse_and_test_diff()
print("\nFailed Code Blocks:")
for pre_code_block, code_block in results["failed_code_blocks"]:
    print("-----")
    print("Original response:")
    print(pre_code_block)
    print("-----")
    print("Modified Code:")
    print(code_block)
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
