import json


def count_tokens(file_path="model_responses.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    token_counts = {}
    token_counts = {"whole": 0, "diff": 0, "udiff": 0}
    for entry in data:
        edit_type = entry['edit_type']
        token_count = entry['response_dict']['usage']['total_tokens']
        token_counts[edit_type] += token_count

    print(token_counts.items())

    return token_counts


count_tokens()
