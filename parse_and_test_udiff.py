import json
import contextlib
import re
import sys

from utils import test_logic, test_crash, test_class_extension, LOGIC_TEST_CODE_SNIPPET, CRASH_TEST_CODE_SNIPPET, CLASS_EXTENSION_TEST_CODE_SNIPPET


def parse_and_test_udiff(file_path="model_responses.json"):
    # Read model_responses.json
    with open("model_responses.json", "r") as f:
        data = json.load(f)

    # Filter responses for a specific edit type - diff
    udiff_edit_responses = [
        entry for entry in data if entry['edit_type'] == 'udiff']

    # print first response
    print(udiff_edit_responses[0]["response"])

    def extract_code_block(response, task):
        response = response
        if response.startswith("```") and response.endswith("```"):
            response = "\n".join(response.split("\n")[1:-1])

        hunk_splits = re.split(r"(^@@.*?@@)", response, re.MULTILINE)

        code_block = None
        if task == "Logic Test":
            code_block = LOGIC_TEST_CODE_SNIPPET
        elif task == "Crash Test":
            code_block = CRASH_TEST_CODE_SNIPPET
        elif task == "Class Extension Test":
            code_block = CLASS_EXTENSION_TEST_CODE_SNIPPET

        for i in range(1, len(hunk_splits), 2):
            if i + 1 >= len(hunk_splits):
                break

            content = hunk_splits[i + 1]

            search_lines = []
            replace_lines = []

            for line in content.split("\n"):
                if line.strip() == "":
                    continue
                if line.startswith("-"):
                    search_lines.append(line[1:])
                elif line.startswith("+"):
                    replace_lines.append(line[1:])
                else:
                    search_lines.append(line)
                    replace_lines.append(line)

            code_lines = code_block.split("\n")
            code_lines = [line for line in code_lines if line.strip() != '']

            search_normalized = [line.strip()
                                 for line in search_lines if line.strip() != '']
            n_search = len(search_normalized)

            if n_search == 0:
                continue

            match_index = -1
            for idx in range(len(code_lines) - n_search + 1):
                window = code_lines[idx:idx + n_search]
                window_normalized = [line.strip() for line in window]

                if window_normalized == search_normalized:
                    match_index = idx
                    break
            if match_index == -1:
                continue
            else:
                code_lines[match_index:match_index + n_search] = replace_lines
                code_block = "\n".join(code_lines)

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

    for entry in udiff_edit_responses:
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


with contextlib.redirect_stdout(sys.stdout):
    results = parse_and_test_udiff()
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
