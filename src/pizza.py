class PizzaState:
    def __init__(self, ingredients=None):
        if ingredients is None:
            ingredients = set()
        self.ingredients = ingredients

    def add_ing(self, ingredient):
        new_ingredients = self.ingredients.copy()
        new_ingredients.add(ingredient)
        return PizzaState(new_ingredients)
    
    def rem_ing(self, ingredient):
        new_ingredients = self.ingredients.copy()
        new_ingredients.remove(ingredient)
        return PizzaState(new_ingredients)

    def __eq__(self, other):
        return self.ingredients == other.ingredients

    def __hash__(self):
        return hash(tuple(sorted(self.ingredients)))

    def __str__(self):
        return str(sorted(self.ingredients))


# Operator - Add Ingredient
def add_ingredient(state, ingredient):
    if ingredient not in state.ingredients:
        return state.add_ing(ingredient)
    return None

# Operator - Remove Ingredient
def remove_ingredient(state, ingredient):
    if ingredient in state.ingredients:
        return state.rem_ing(ingredient)
    return None


