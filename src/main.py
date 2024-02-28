import utils
import pizza


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

    
# Main function
def main():
    display_title()

    file_name = select_file()
    
    utils.read_input_file(file_name)
    
    #algorithm_choice = select_algorithm()
    
    #print(f"Running {algorithms[algorithm_choice]} algorithm...")

    # Here we would call the selected algorithm function

    # For now, we will just run the Breadth First Search algorithm
    goal = utils.breadth_first_search(pizza.PizzaState(), 
                           utils.goal_pizza_state, 
                            utils.child_pizza_states)
    
    # Print the goal state and the solution
    print(goal.state)
    utils.print_solution(goal)

main() 