import utils
import app


# List of possible algorithms
algorithms = ["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"]
# List of possible input files
files = ["a_an_example.in.txt", "b_basic.in.txt", "c_coarse.in.txt", "d_difficult.in.txt", "e_elaborate.in.txt"]
# List of possible parameters
parameters = {"temperature": 100, "cooling_rate": 0.001, "max_iter": 1000, "max_no_improv": 20, "aspiration": 1, "tenure": 20, "population_size": 20, "generations": 50, "mutation_rate": 0.2}

# Set the file to be used
def set_file(choice):
    global file_name
    if 0 <= choice <= 4:
        file_name = f"../data/{files[choice]}"

# Set the algorithm to be used
def set_algorithm(choice):
    global chosen_algorithm
    if 0 <= choice <= 3:
        chosen_algorithm = choice

# Set the parameters to be used
def set_parameters(chosen_parameters):
    global parameters
    # Update only the parameters that were changed, keep the default for the rest
    parameters.update(chosen_parameters)

# Start the chosen algorithm
def start_algorithm(update_solution_and_score, insert_output):
    print(f"Running {algorithms[chosen_algorithm]} algorithm...")
    print(f"Using file: {file_name}")
    print(f"Using parameteres: {parameters}")
    # Output the chosen algorithm and file being used
    insert_output(f"Running {algorithms[chosen_algorithm]} algorithm...\nUsing file: {file_name}\nUsing parameteres: {parameters}\n\n")
    # Read the input file
    utils.read_input_file(file_name)

    if chosen_algorithm == 0:
        solution, score = utils.hill_climbing_algorithm(update_solution_and_score, insert_output)
    elif chosen_algorithm == 1:
        solution, score = utils.simulated_annealing_algorithm(update_solution_and_score, insert_output, 
                                                              temperature=parameters["temperature"], 
                                                              cooling_rate=parameters["cooling_rate"])
    elif chosen_algorithm == 2:
        solution, score = utils.run_tabu_search(update_solution_and_score, insert_output,
                                                max_iter=parameters["max_iter"], 
                                                max_no_improv=parameters["max_no_improv"],
                                                aspiration=parameters["aspiration"], 
                                                tenure=parameters["tenure"])
    elif chosen_algorithm == 3:
        solution, score, _ = utils.genetic_algorithm(utils.clients, utils.unique_ingredients, 
                                                        population_size=parameters["population_size"],
                                                        generations=parameters["generations"],
                                                        mutation_rate=parameters["mutation_rate"],
                                                       update_solution_and_score=update_solution_and_score,
                                                       insert_output=insert_output)

    
    return solution, score
    

# Main function
def main():
    app.run_app(start_algorithm=start_algorithm, set_file=set_file, set_algorithm=set_algorithm, set_parameters=set_parameters)


main() 