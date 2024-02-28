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

def add_ingredient(state, ingredient):
    if ingredient not in state.ingredients:
        return state.add_ing(ingredient)
    return None

def remove_ingredient(state, ingredient):
    if ingredient in state.ingredients:
        return state.rem_ing(ingredient)
    return None

def objective_test(state, clients):
    satisfied_clients = 0
    for client_likes, client_dislikes in clients:
        if all(ingredient in state.ingredients for ingredient in client_likes) and \
                not any(ingredient in state.ingredients for ingredient in client_dislikes):
            satisfied_clients += 1
    return satisfied_clients

# Usage:
# Define initial state
initial_state = PizzaState()

# Define clients' preferences
clients = [
    (["cheese", "peppers"], []),
    (["basil"], ["pineapple"]),
    (["mushrooms", "tomatoes"], ["basil"])
]

# Add an ingredient to the state
new_state = add_ingredient(initial_state, "cheese")
new_state = add_ingredient(new_state, "peppers")
new_state = add_ingredient(new_state, "basil")


# Check objective test
score = objective_test(new_state, clients)
print("Score:", score)