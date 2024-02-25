# Definition of the Client class that contaains the list of ingredients the client likes and dislikes
class Client:
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

# List to store all clients
clients = []

# Set to store all unique ingredients mentioned by the clients
unique_ingredients = set()

# Set to store the ingredients selected for the pizza
pizza_ingredients = set()


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
    pizza_ingredients.clear()
