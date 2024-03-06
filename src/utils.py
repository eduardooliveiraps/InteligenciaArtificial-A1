from collections import deque
import pizza
import pygad
import random

# Definition of the Client class that contaains the list of ingredients the client likes and dislikes
class Client:
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

# List to store all clients
clients = []

# Set to store all unique ingredients mentioned by the clients
unique_ingredients = set()

# Solution that represents a unique pizza state
solution = pizza.PizzaState()

# Score of the solution
score = 0

# Function to read the input file and store the data in the clients list
def read_input_file(filename):
    # Open the file for reading
    with open(filename, 'r') as file:
        # Read the number of clients from the first line of the file and convert to an integer
        num_clients = int(file.readline().strip())
        
        # Iterate over each remaining line in the file
        for _ in range(num_clients):
            # Read the client's ingredient preferences and split them into likes and dislikes
            line_likes = set(file.readline().strip().split()[1:])
            line_dislikes = set(file.readline().strip().split()[1:])
            
            # Create an instance of the Client class with the read preferences and add it to the clients list
            clients.append(Client(line_likes, line_dislikes))
            
            # Add the client's liked and disliked ingredients to the unique ingredients set
            unique_ingredients.update(line_likes)
            unique_ingredients.update(line_dislikes)

# Function to clear the data structures
def clear_data():
    clients.clear()
    unique_ingredients.clear()
    solution = pizza.PizzaState()
    score = 0

# Operators for the pizza problem
def child_pizza_states(state):
    new_states = []
    for ingredient in unique_ingredients:
        add_state = pizza.add_ingredient(state, ingredient)
        if add_state:
            new_states.append(add_state)
        rem_state = pizza.remove_ingredient(state, ingredient)
        if rem_state:
            new_states.append(rem_state)
    return new_states

# Objective function for the pizza problem
def objective_test(state, clients):
    satisfied_clients = 0
    for client in clients:
        if all(ingredient in state.ingredients for ingredient in client.likes) and \
                not any(ingredient in state.ingredients for ingredient in client.dislikes):
            satisfied_clients += 1
    return satisfied_clients

# Goal State Function
def goal_pizza_state(state):
    return pizza.objective_test(state, clients) == 2

# Print the solution found
def print_solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    for state in path:
        print(state)
    return

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self



##############
# ALGORITHMS #
##############

# Breadth First Search Algorithm
def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    
    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node
        
        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            child = TreeNode(state)
            
            # link child node to its parent in the tree
            node.add_child(child)
            
            # enqueue the child node
            queue.append(child)
            

    return None


# Gentic Algorithm
def evaluate(pizza: set[str]) -> int:
    global clients
    result = 0
    for c in clients:
        if c.likes & pizza == c.likes and c.dislikes & pizza == set():
            result += 1
    return result

def genetic_algorithm(generations=2000):
        global clients, unique_ingredients, score, solution

        ingredients_list = sorted(list(unique_ingredients))

        def fitness_func(ga_instance, solution, solution_idx):
            pizza = set([ingredients_list[k] for (k,v) in enumerate(solution) if v == 1])
            return evaluate(pizza)

        ga_instance = pygad.GA(
            num_generations=generations,
            num_parents_mating=2,
            sol_per_pop=3,
            num_genes=len(ingredients_list),
            fitness_func=fitness_func,
            init_range_low=0,
            init_range_high=2,
            random_mutation_min_val=0,
            random_mutation_max_val=2,
            mutation_by_replacement=True,
            gene_type=int)

        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        solution = set([ingredients_list[k] for (k,v) in enumerate(solution) if v == 1])
        score = solution_fitness

        return solution, score
    
# Neighborhood Function for the Tabu Algorithm
def improved_child_pizza_states(state, tabu_list):
    global unique_ingredients
    new_states = []

    # Explore addition/removal of ingredients
    for ingredient in unique_ingredients:
        add_state = pizza.add_ingredient(state, ingredient)
        if add_state and add_state not in tabu_list:
            new_states.append(add_state)
        rem_state = pizza.remove_ingredient(state, ingredient)
        if rem_state and rem_state not in tabu_list:
            new_states.append(rem_state)
    
    return new_states

# Tabu Search Algorithm
def tabu_search(initial_solution, objective_function, neighborhood_function, max_iterations=1000, tabu_tenure=10, aspiration_threshold=1):
    global clients
    # Initialize tabu list
    tabu_list = []
    
    # Initialize current solution
    current_solution = initial_solution
    
    # Initialize best solution
    best_solution = current_solution
    best_score = objective_function(best_solution, clients)
    
    # Tabu search algorithm
    for i in range(max_iterations):
        # Generate neighboring solutions
        neighbors = neighborhood_function(current_solution, tabu_list)
        
        # Filter out tabu solutions
        non_tabu_neighbors = [neighbor for neighbor in neighbors if neighbor not in tabu_list]
        
        # Evaluate neighbor solutions
        neighbor_scores = [(neighbor, objective_function(neighbor, clients)) for neighbor in neighbors]
        non_tabu_neighbor_scores = [(neighbor, objective_function(neighbor, clients)) for neighbor in non_tabu_neighbors]
        
        # Select the best neighbor solution
        neighbor_scores.sort(key=lambda x: x[1], reverse=True)
        best_neighbor, best_neighbor_score = neighbor_scores[0]

        # Select the best non-tabu neighbor solution
        non_tabu_neighbor_scores.sort(key=lambda x: x[1], reverse=True)
        best_non_tabu_neighbor, best_non_tabu_neighbor_score = non_tabu_neighbor_scores[0]

        # Check if the best solution is a superior move and is on the tabu list
        if best_neighbor_score > best_score and best_neighbor in tabu_list:
            # Apply aspiration criteria
            if best_neighbor_score - best_score > aspiration_threshold:
                current_solution = best_neighbor
                best_solution = best_neighbor
                best_score = best_neighbor_score
            else:
                current_solution = best_non_tabu_neighbor
                best_solution = current_solution
                best_score = best_non_tabu_neighbor_score
        else:
            # Apply the best non-tabu move
            current_solution = best_non_tabu_neighbor
            best_solution = current_solution
            best_score = best_non_tabu_neighbor_score

        # Add current solution to tabu list
        tabu_list.append(current_solution)
        
        # Maintain tabu list size
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
        
        # Check termination condition (e.g., no improvement for several iterations)
        # Terminate if the termination condition is met
        # In this example, we'll terminate if no improvement is observed after 100 iterations
        if i > 100 and best_neighbor_score == best_score:
            break
    
    return best_solution, best_score


def run_tabu_search():
    initial_solution = pizza.PizzaState()
    best_solution, best_score = tabu_search(initial_solution, objective_test, improved_child_pizza_states, aspiration_threshold=2)

    return best_solution, best_score

