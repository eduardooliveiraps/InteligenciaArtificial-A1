import pizza
import pygad
import random
import math
from collections import deque

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
    global clients, unique_ingredients
    # Clear the data structures
    clear_data()
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

##############
# ALGORITHMS #
##############

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self        

# Generate a random starting state        
def generate_starting_state(clients):
    selected_client = random.choice(clients)
    ingredients = selected_client.likes
    return pizza.PizzaState(ingredients)

# Objective test for the pizza problem
def objective_test(state, clients):
    satisfied_clients = 0
    for client in clients:
        if all(ingredient in state.ingredients for ingredient in client.likes) and \
                not any(ingredient in state.ingredients for ingredient in client.dislikes):
            satisfied_clients += 1
    return satisfied_clients
    

###########
# Genetic #
###########


# Evaluate the fitness of a pizza
def evaluate(pizza: set[str]) -> int:
    global clients
    result = 0
    for c in clients:
        if c.likes & pizza == c.likes and c.dislikes & pizza == set():
            result += 1
    return result

# Genetic Algorithm
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

def genetic_algorithm2(clients, unique_ingredients, population_size=20, generations=50, mutation_rate=0.2, update_solution_and_score=None, insert_output=None):
    num_ingredients = len(unique_ingredients)
    population = create_initial_population(population_size, num_ingredients)
    
    best_individual_per_generation = []  # Lista para manter o melhor indivíduo de cada geração
    
    for generation in range(generations):
        unique_ingredients = list(unique_ingredients)
        scores = [evaluate2([unique_ingredients[i] for i, gene in enumerate(solution) if gene], clients) for solution in population]
        best_solution_idx = scores.index(max(scores))
        best_solution = [unique_ingredients[i] for i, gene in enumerate(population[best_solution_idx]) if gene]
        
        # Adicione o melhor indivíduo desta geração ao registro
        best_individual_per_generation.append((best_solution, max(scores)))
        
        # Chame a função para atualizar o melhor indivíduo e sua pontuação
        if update_solution_and_score:
            update_solution_and_score(best_solution, max(scores))
        
        output_message = f"Generation {generation + 1}: {best_solution}\nScore: {max(scores)}\n\n"

        if insert_output:
            insert_output(output_message)
        
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
    
    return best_solution, best_score, best_individual_per_generation


###############
# Tabu Search #
###############


# Run Tabu Search Algorithm
def run_tabu_search(update_solution_and_score=None, insert_output=None, max_iter=1000, max_no_improv=20, aspiration=1, tenure=15,):
    initial_solution = generate_starting_state(clients)
    # Output the initial solution
    if insert_output:
        insert_output(f"Initial Solution: {initial_solution}\n\n")
    best_solution, best_score = tabu_search(initial_solution, objective_test, child_pizza_states, max_iterations=max_iter, max_no_improv=max_no_improv, tabu_tenure=tenure, aspiration_threshold=aspiration, update_solution_and_score=update_solution_and_score, insert_output=insert_output)

    return best_solution, best_score 

# Neighborhood Function for the Tabu Algorithm
def child_pizza_states(state, tabu_list):
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
def tabu_search(initial_solution, objective_function, neighborhood_function, max_iterations=1000, max_no_improv=20, tabu_tenure=10, aspiration_threshold=1, update_solution_and_score=None, insert_output=None):
    global clients
    # Initialize tabu list
    tabu_list = []
    
    # Initialize current solution
    current_solution = initial_solution
    
    # Initialize best solution
    best_solution = current_solution
    best_score = objective_function(best_solution, clients)

    # Set the current solution and score
    if update_solution_and_score:
        update_solution_and_score(best_solution, best_score)

    same_score_iteration = 0

    # Tabu search algorithm
    for i in range(int(max_iterations)):
        # Output the current solution and best score
        if insert_output:
            insert_output(f"Iteration {i}: {current_solution}\nScore: {objective_function(current_solution, clients)}\n\n")
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
        if best_neighbor_score > best_score:
            same_score_iteration = 0
            # Apply aspiration criteria
            if best_neighbor in tabu_list and best_neighbor_score - best_score > int(aspiration_threshold):
                if insert_output:
                    insert_output("Aspiration criteria applied!\n\n")
                current_solution = best_neighbor
                best_solution = best_neighbor
                best_score = best_neighbor_score
            else:
                # Apply the best non-tabu move
                current_solution = best_non_tabu_neighbor
                best_solution = best_non_tabu_neighbor
                best_score = best_non_tabu_neighbor_score
        else:
            # Apply the best non-tabu move
            current_solution = best_non_tabu_neighbor


        # Add current solution to tabu list
        tabu_list.append(current_solution)

        # Update the current solution and score
        if update_solution_and_score:
            update_solution_and_score(best_solution, best_score)
        
        # Maintain tabu list size
        if len(tabu_list) > int(tabu_tenure):
            tabu_list.pop(0)
        
        same_score_iteration += 1

        # Check termination condition (e.g., no improvement for several iterations)
        # Terminate if the termination condition is met
        # In this example, we'll terminate if no improvement is observed after max_no_improv iterations
        if same_score_iteration > int(max_no_improv) and best_neighbor_score == best_score:
            break
    
    return best_solution, best_score


#################
# Hill Climbing #
#################


# Generate the best neighbor
def generate_best_neighbor(cur_solution, cur_solution_score):
    b_neighbor = cur_solution
    b_neighbor_score = cur_solution_score

    # Generate neighbors by adding one missing ingredient to the current solution
    for ingredient in unique_ingredients:
        if ingredient not in cur_solution.ingredients:
            new_neighbor = cur_solution.add_ing(ingredient)
            if((objective_test(new_neighbor, clients) > b_neighbor_score)):
                b_neighbor = new_neighbor
                b_neighbor_score = objective_test(new_neighbor, clients)
    # Generate neighbors by removing one ingredient from the current solution
    for ingredient in unique_ingredients:
        if ingredient in cur_solution.ingredients:
            new_neighbor = cur_solution.rem_ing(ingredient)
            if((objective_test(new_neighbor, clients) > b_neighbor_score)):
                b_neighbor = new_neighbor
                b_neighbor_score = objective_test(new_neighbor, clients)

    return b_neighbor, b_neighbor_score

# Hill Climbing Algorithm
def hill_climbing_algorithm(update_solution_and_score=None, insert_output=None):
    global clients, unique_ingredients, score

    current_solution = generate_starting_state(clients)

    if insert_output:
        insert_output(f"Initial Solution: {current_solution}\n\n")
    current_score = objective_test(current_solution, clients)

    best_neighbor = current_solution
    best_neighbor_score = current_score

    # Set the current solution and score
    if update_solution_and_score:
        update_solution_and_score(best_neighbor, best_neighbor_score)

    i = 0
    while True:
        best_neighbor, best_neighbor_score = generate_best_neighbor(current_solution, current_score)

        # Terminate if no better neighbor is found
        if best_neighbor_score <= current_score:
            if insert_output:
                insert_output("Terminating: No better neighbor found\n\n")
            break

        # Update the current solution and score
        current_solution = best_neighbor
        current_score = best_neighbor_score

        # Output the current solution and best score
        if insert_output:
            insert_output(f"Iteration {i}: {current_solution}\nScore: {current_score}\n\n")
        
        # Set the current solution and score
        if update_solution_and_score:
            update_solution_and_score(current_solution, current_score)

        i += 1

    # Set the solution and score
    solution = current_solution
    score = current_score

    return solution, score


########################
# Simbulated Annealing #
########################


# Generate neighbors
def generate_neighbors(solution):
    neighbors = []
    # Generate neighbors by adding one missing ingredient to the current solution
    for ingredient in unique_ingredients:
        if ingredient not in solution.ingredients:
            new_neighbor = solution.add_ing(ingredient)
            neighbors.append(new_neighbor)

    # Generate neighbors by removing one ingredient from the current solution
    for ingredient in solution.ingredients:
        if ingredient in solution.ingredients:
            new_neighbor = solution.rem_ing(ingredient)
            neighbors.append(new_neighbor)

    return neighbors

# Acceptance Probability Function
def acceptance_probability_function(current_score, new_score, temperature):
    if new_score > current_score:
        return 1
    return pow(math.e, (new_score - current_score) / temperature) / 1.5

# Simulated Annealing Algorithm
def simulated_annealing_algorithm(update_solution_and_score=None, insert_output=None, temperature=100, cooling_rate=0.001):
    global clients, unique_ingredients, score

    current_solution = generate_starting_state(clients)
    current_score = objective_test(current_solution, clients)

    # Output the initial solution
    if insert_output:
        insert_output(f"Initial Solution: {current_solution}\n\n")

    best_solution = current_solution
    best_score = current_score

    # Set the current solution and score
    if update_solution_and_score:
        update_solution_and_score(best_solution, best_score)

    counter = 0  # initialize counter

    i = 0
    while temperature > 1:
        neighbors = generate_neighbors(current_solution)

        new_solution = random.choice(neighbors)
        new_score = objective_test(new_solution, clients)

        # Output the current solution and best score
        if insert_output:
            insert_output(f"Iteration {i}: {current_solution}\nBest Score: {current_score}\n\n")

        acceptance_probability = acceptance_probability_function(current_score, new_score, temperature)

        if counter >= 100:  # break the loop if solution hasn't changed for 100 iterations
            break

        if new_score > current_score or random.random() < acceptance_probability:
            current_solution = new_solution
            current_score = new_score
            counter = 0  # reset counter if solution changes

        if new_score > best_score:
            best_solution = new_solution
            best_score = new_score

        else:
            counter += 1  # increment counter if solution doesn't change

        temperature *= 1 - cooling_rate

        i += 1

        # Update the best solution and score
        if update_solution_and_score:
            update_solution_and_score(best_solution, best_score)

    solution = best_solution
    score = best_score

    return solution, score
    