import utils
import warnings
import pygame
import pygame_menu

warnings.filterwarnings("ignore", category=UserWarning, module="pygad")


# List of possible algorithms
algorithms = ["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"]
# List of possible input files
files = ["a_an_example.in.txt", "b_basic.in.txt", "c_coarse.in.txt", "d_difficult.in.txt", "e_elaborate.in.txt"]

# Function to display the title of the program
def display_title():
    print("******************************************")
    print("*    One Pizza - Optimization Problem    *")
    print("******************************************\n")


# Function to select a file from the list of possible input files
def select_file():
    print("Select a file:")
    print("     1. a_an_example.in.txt")
    print("     2. b_basic.in.txt")
    print("     3. c_coarse.in.txt")
    print("     4. d_difficult.in.txt")
    print("     5. e_elaborate.in.txt")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 5:
                return f"../data/{files[choice - 1]}"
            else:
                print("Invalid choice. Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid choice. Please enter a number.")


# Function to select an algorithm from the list of possible algorithms
def select_algorithm():
    print("Select an algorithm:")
    for i, algorithm in enumerate(algorithms, 1):
        print(f"{i}. {algorithm}")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(algorithms):
                return choice - 1
            else:
                print("Invalid choice. Please enter a number between 1 and", len(algorithms))
        except ValueError:
            print("Invalid choice. Please enter a number.")

def set_file(_, choice):
    global file_name
    if 0 <= choice <= 4:
        file_name = f"../data/{files[choice]}"

def set_algorithm(_, choice):
    global chosen_algorithm
    if 0 <= choice <= 3:
        chosen_algorithm = choice

def start_algorithm():
    global state, solution, score
    print(f"Running {algorithms[chosen_algorithm]} algorithm...")
    utils.read_input_file(file_name)

    if chosen_algorithm == 0:
        print ("Hill Climbing")
        solution, score = 1, 1
        #solution, score = utils.hill_climbing()
    elif chosen_algorithm == 1:
        print ("Simulated Annealing")
        solution, score = 1, 1
       #solution, score = utils.simulated_annealing()
    elif chosen_algorithm == 2:
        solution, score = utils.run_tabu_search()
    elif chosen_algorithm == 3:
        solution, score = utils.genetic_algorithm()
    
    state = 1


# Initialize the game menu
def init_menu():
    menu = pygame_menu.Menu('Welcome', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)

    menu.add.dropselect('File :', [('Example', 0), ('Basic', 1), ('Coarse', 2), ('Dificult', 3), ('Elaborate', 4)], onchange=set_file)
    menu.add.dropselect('Algorithm :', [('Hill Climbing', 0), ('Simulated Annealing', 1), ('Tabu Search', 2), ('Genetic Algorithm', 3)], onchange=set_algorithm)
    menu.add.button('Run', start_algorithm)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    return menu
    
# Draw the final solution and score
def solution_menu(solution, score):
    menu = pygame_menu.Menu('Solution', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)
    menu.add.label(f"Best solution: {solution}")
    menu.add.label(f"Score: {score}")
    menu.add.button('Quit', pygame_menu.events.EXIT)
    return menu
    

# Main function
def main():
    global state, solution, score
    state = 0
    pygame.init()
    surface = pygame.display.set_mode((1000, 700))
    menu = init_menu()
    menu.mainloop(surface)


main() 