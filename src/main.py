import utils
import warnings
import pygame
import pygame_menu
import menu

warnings.filterwarnings("ignore", category=UserWarning, module="pygad")


# List of possible algorithms
algorithms = ["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"]
# List of possible input files
files = ["a_an_example.in.txt", "b_basic.in.txt", "c_coarse.in.txt", "d_difficult.in.txt", "e_elaborate.in.txt"]

def set_file(_, choice):
    global file_name
    if 0 <= choice <= 4:
        file_name = f"../data/{files[choice]}"

def set_algorithm(_, choice):
    global chosen_algorithm
    if 0 <= choice <= 3:
        chosen_algorithm = choice

def start_algorithm(algorithm):
    print(f"Running {algorithms[chosen_algorithm]} algorithm...")
    utils.read_input_file(file_name)

    if chosen_algorithm == 0:
        print ("Hill Climbing")
        solution, score = utils.hill_climbing_algorithm()
    elif chosen_algorithm == 1:
        print ("Simulated Annealing")
        solution, score = utils.simulated_annealing_algorithm()
    elif chosen_algorithm == 2:
        solution, score = utils.run_tabu_search(algorithm)
    elif chosen_algorithm == 3:
        solution, score = utils.genetic_algorithm()
    
    return solution, score
    

# Main function
def main():
    menu_state_manager = menu.MenuStateManager(start_algorithm=start_algorithm, set_file=set_file, set_algorithm=set_algorithm)
    menu_state_manager.render()



main() 