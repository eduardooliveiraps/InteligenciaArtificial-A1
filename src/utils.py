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
    

# Genetic Algorithm without using the pygad library

def evaluate2(pizza, clients):
    score = 0
    for client in clients:
        if client.likes.issubset(pizza) and not client.dislikes.intersection(pizza):
            score += 1
    return score

def create_initial_population(population_size, num_ingredients):
    population = []
    for _ in range(population_size):
        pizza = [random.randint(0, 1) for _ in range(num_ingredients)]
        population.append(pizza)
    return population

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(solution, mutation_rate):
    mutated_solution = []
    for gene in solution:
        if random.random() < mutation_rate:
            mutated_solution.append(1 - gene)
        else:
            mutated_solution.append(gene)
    return mutated_solution

def select_parents(population, scores):
    total_score = sum(scores)
    probabilities = [score / total_score for score in scores]
    parent_indices = random.choices(range(len(population)), weights=probabilities, k=2)
    while parent_indices[0] == parent_indices[1]:  # Ensure unique parents
        parent_indices = random.choices(range(len(population)), weights=probabilities, k=2)
    return population[parent_indices[0]], population[parent_indices[1]]

def genetic_algorithm2(clients, unique_ingredients, population_size=20, generations=50, mutation_rate=0.2):
    num_ingredients = len(unique_ingredients)
    population = create_initial_population(population_size, num_ingredients)
    
    for _ in range(generations):
        unique_ingredients = list(unique_ingredients)
        scores = [evaluate2([unique_ingredients[i] for i, gene in enumerate(solution) if gene], clients) for solution in population]
        best_solution_idx = scores.index(max(scores))
        best_solution = [unique_ingredients[i] for i, gene in enumerate(population[best_solution_idx]) if gene]
        
        print("Generation:", _ + 1, "Best solution:", best_solution, "Score:", max(scores))
        
        new_population = [population[best_solution_idx]]
        
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    best_solution_idx = scores.index(max(scores))
    best_solution = [unique_ingredients[i] for i, gene in enumerate(population[best_solution_idx]) if gene]
    best_score = max(scores)
    
    return best_solution, best_score