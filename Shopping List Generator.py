"""
SHOPPING LIST GENERATOR

Whenever I meal prep, I deal with a lot of recipes that overlap in terms of their ingredients.
This simple program combines all your recipes into a single shopping list.
"""

import re
from collections import defaultdict

class ShoppingListGenerator:
    def __init__(self):
        self.shopping_list = defaultdict(int)

    def parse_input(self, user_input):
        items = [item.strip() for item in re.split(",|\n", user_input)]
        for item in items:
            match = re.match(r'(\w+)\s*(\d*)', item)
            if match:
                ingredient, quantity = match.groups()
                quantity = int(quantity) if quantity else 1
                yield ingredient.lower(), quantity

    def add_recipe(self):
        while True:
            user_input = input("> ")
            if 'done' in user_input.lower():
                for ingredient, quantity in self.parse_input(user_input):
                    self.shopping_list[ingredient] += quantity
                break
            else:
                for ingredient, quantity in self.parse_input(user_input):
                    self.shopping_list[ingredient] += quantity

    def generate_shopping_list(self):
        print("Enter recipes. Type 'done' when you've entered all ingredients for a recipe.")
        print("Format:\n'item quantity, item 2 quantity 2, done' \n'item quantity' <return> 'item 2 quantity 2' <return> ... 'done'")
        while True:
            self.add_recipe()
            if input("Would you like to add another recipe? (y/n)").lower() != 'y':
                break

        print("\nShopping List:")
        for item, quantity in self.shopping_list.items():
            if item != "done":
                print(f"{item}: {quantity}")

if __name__ == "__main__":
    s = ShoppingListGenerator()
    s.generate_shopping_list()
