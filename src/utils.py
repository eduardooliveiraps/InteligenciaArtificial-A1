from collections import deque
import pizza

# Definition of the Client class that contaains the list of ingredients the client likes and dislikes
class Client:
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

# List to store all clients
clients = []

# Set to store all unique ingredients mentioned by the clients
unique_ingredients = set()


# Function to read the input file and store the data in the clients list
def read_input_file(filename):
    # Open the file for reading
    with open(filename, 'r') as file:
        # Read the number of clients from the first line of the file and convert to an integer
        num_clients = int(file.readline().strip())
        
        # Iterate over each remaining line in the file
        for _ in range(num_clients):
            # Read the client's ingredient preferences and split them into likes and dislikes
            line_likes = file.readline().strip().split()[1:]
            line_dislikes = file.readline().strip().split()[1:]
            
            # Create an instance of the Client class with the read preferences and add it to the clients list
            clients.append(Client(line_likes, line_dislikes))
            
            # Add the client's liked and disliked ingredients to the unique ingredients set
            unique_ingredients.update(line_likes)
            unique_ingredients.update(line_dislikes)

# Function to clear the data structures
def clear_data():
    clients.clear()
    unique_ingredients.clear()

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