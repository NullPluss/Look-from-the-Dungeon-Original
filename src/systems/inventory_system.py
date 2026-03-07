from collections import defaultdict

class Inventory:
    def __init__(self):
        self.items = defaultdict(int)
    
    def add_item(self, item_name, count=1):
        self.items[item_name] += count
    
    def remove_item(self, item_name, count=1):
        if self.items[item_name] >= count:
            self.items[item_name] -= count
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        return False
    
    def get_items(self):
        return dict(self.items)

class InventorySystem:
    """
    Логика управления предметами.
    """

    def use_item(self, party, item):
        pass