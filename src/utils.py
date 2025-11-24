LOGIC_TEST_CODE_SNIPPET = """
def calculate_median(numbers):
    \"\"\"
    Calculates the median of a list of numbers.
    \"\"\"
    if not numbers:
        return None

    n = len(numbers)
    mid_index = n // 2

    if n % 2 == 1:
        return numbers[mid_index]
    else:
        return (numbers[mid_index - 1] + numbers[mid_index]) / 2
"""

CRASH_TEST_CODE_SNIPPET = """
def process_user_ids(user_ids):
    print(f"Processing {len(user_ids)} users...")

    for i in range(len(user_ids) + 1):
        current_id = user_ids[i]
        # Simulate processing
        processed_id = current_id * 1000
        print(f"User ID {current_id} processed as {processed_id}")
"""

CLASS_EXTENSION_TEST_CODE_SNIPPET = """
class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_stock(self, item_name, quantity):
        \"\"\"Adds stock for a specific item.\"\"\"
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        print(f"Added {quantity} of {item_name}.")

    def check_stock(self, item_name):
        \"\"\"Returns the current stock of an item.\"\"\"
        return self.inventory.get(item_name, 0)
"""


def test_logic(code_block):
    code_block += ("\ndata=[10,2,5]\nresult=calculate_median(data)")
    local_scope = {}
    try:
        exec(code_block, {}, local_scope)
        if local_scope.get("result") == 5:
            return True
        else:
            return False
    except Exception:
        return False


def test_crash(code_block):
    code_block += ("\nids=[1,2,3,4,5]\nprocess_user_ids(ids)")
    try:
        exec(code_block, {}, {})
        return True
    except Exception:
        return False


def test_class_extension(code_block):
    code_block += ("\nstore=InventoryManager()\nstore.add_stock('apple',10)\nstore.remove_stock('apple',4)\ncurrent_stock=store.check_stock('apple')")
    local_scope = {}
    try:
        exec(code_block, {}, local_scope)
        if local_scope.get("current_stock") == 6:
            return True
        else:
            return False
    except Exception:
        return False
