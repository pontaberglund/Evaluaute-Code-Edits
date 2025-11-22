class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_stock(self, item_name, quantity):
        """Adds stock for a specific item."""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        print(f"Added {quantity} of {item_name}.")

    def check_stock(self, item_name):
        """Returns the current stock of an item."""
        return self.inventory.get(item_name, 0)
