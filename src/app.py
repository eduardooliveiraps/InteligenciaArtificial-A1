import customtkinter
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, start_algorithm, set_file, set_algorithm, set_parameters, width=1280, heigh=720):
        super().__init__()
        self.start_algorithm = start_algorithm
        self.set_file = set_file
        self.set_algorithm = set_algorithm
        self.set_parameters = set_parameters

        # configure window
        self.title("One Pizza")
        self.geometry(f"{width}x{heigh}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="One Pizza", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.dev_label = customtkinter.CTkLabel(self.sidebar_frame, text="Developed by:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.dev_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.dev_name_1 = customtkinter.CTkLabel(self.sidebar_frame, text="Eduardo Oliveira", font=customtkinter.CTkFont(size=16, weight="normal"))
        self.dev_name_1.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.dev_name_2 = customtkinter.CTkLabel(self.sidebar_frame, text="João Francisco Alves", font=customtkinter.CTkFont(size=16, weight="normal"))
        self.dev_name_2.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.dev_name_3 = customtkinter.CTkLabel(self.sidebar_frame, text="José Miguel Isidro", font=customtkinter.CTkFont(size=16, weight="normal"))
        self.dev_name_3.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", font=customtkinter.CTkFont(size=16, weight="normal"), anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(30, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       font=customtkinter.CTkFont(size=16, weight="normal"),
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", font=customtkinter.CTkFont(size=16, weight="normal"), anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               font=customtkinter.CTkFont(size=16, weight="normal"),
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox for One Pizza Problem
        self.textbox = customtkinter.CTkTextbox(self, width=250, font=customtkinter.CTkFont(size=14, weight="normal"))
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create textbox for output
        self.output = customtkinter.CTkTextbox(self, width=250, font=customtkinter.CTkFont(size=14, weight="normal"))
        self.output.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create options and progressbar frame
        self.options_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.options_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.optionmenu_file = customtkinter.CTkOptionMenu(self.options_frame,
                                                        font=customtkinter.CTkFont(size=16, weight="normal"),
                                                        command=self.option_file_callback,
                                                        values=["Example", "Basic", "Coarse", "Dificult", "Elaborate"])
        self.optionmenu_file.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_algorithm = customtkinter.CTkOptionMenu(self.options_frame,
                                                        font=customtkinter.CTkFont(size=16, weight="normal"),
                                                        command=self.option_algorthim_callback,
                                                        values=["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"])
        self.optionmenu_algorithm.grid(row=0, column=1, padx=20, pady=(20, 10))
        self.param_button = customtkinter.CTkButton(self.options_frame, text="Parameters",
                                                        font=customtkinter.CTkFont(size=20, weight="normal"), 
                                                        command=self.param_button_callback)
        self.param_button.grid(row=1, column=0, padx=20, pady=(50, 10), sticky="ew")
        self.run_button = customtkinter.CTkButton(self.options_frame, text="Run",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"), 
                                                        command=self.run_button_callback)
        self.run_button.grid(row=1, column=1, padx=20, pady=(50, 10), sticky="ew")
        self.clear_button = customtkinter.CTkButton(self.options_frame, text="Clear All",
                                                        font=customtkinter.CTkFont(size=16, weight="normal"), 
                                                        command=self.clear)
        self.clear_button.grid(row=0, column=2, padx=10, pady=(20, 10), sticky="ew")
        self.progress_bar = customtkinter.CTkProgressBar(self.options_frame)
        self.progress_bar.grid(row=2, column=2, padx=10, pady=(50, 10), sticky="ew")
        self.time_label = customtkinter.CTkLabel(self.options_frame, text="Elapsed Time:", font=customtkinter.CTkFont(size=16, weight="normal"))
        self.time_label.grid(row=2, column=0, padx=20, pady=(20, 10))
        self.time = customtkinter.CTkLabel(self.options_frame, text="0.0 s", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.time.grid(row=2, column=1, padx=20, pady=(20, 10))
        self.solution_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.solution_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.solution = customtkinter.CTkTextbox(self.solution_frame, width=300, font=customtkinter.CTkFont(size=14, weight="normal"))
        self.solution.grid(row=0, column=1, padx=20, pady=(10, 10), sticky="ew")
        self.score = customtkinter.CTkLabel(self.solution_frame, text="The Score", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.score.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="ew")

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_file.set("Select File")
        self.optionmenu_algorithm.set("Select Algorithm")
        self.textbox.insert("0.0", "One Pizza Problem\n\n" 
                            + "You are opening a small pizzeria. In fact, your pizzeria is so small that you decided to offer only one type of pizza.\nNow you need to decide what ingredients to include (peppers? tomatoes?both?).\nEveryone has their own pizza preferences.\nEach of your potential clients has some ingredientsthey like, and maybe some ingredients they dislike.\nEach client will come to your pizzeria if both conditions are true:\n\n  1. all the ingredients they like are on the pizza\n  2. none of the ingredients they dislike are on the pizza.\n\n" 
                            + "You want to maximize the number of clients that will come to your pizzeria.\n" + "The problem is to decide what ingredients to include in the pizza.\n\n" 
                            + "PLEASE READ THE INSTRUCTIONS FOR FURTHER DETAILS.\n\n"
                            + "Instructions:\n\n" 
                            + "Each algorithm has its own parameters.\n\n"
                            + "Each parameter should be separated by a comma.\n\n"
                            + "For the Simulated Annealing, the parameters are:\n\n"
                            + "  - temperature: (float) the initial temperature.\n"
                            + "  - cooling_rate: (float) the cooling rate.\n\n"
                            + "For the Tabu Search, the parameters are:\n\n"
                            + "  - max_iter: (integer) the maximum number of iterations.\n"
                            + "  - max_no_improv: (integer) the maximum number of iterations without improvement.\n"
                            + "  - tenure: (integer) the tabu tenure (size of the tabu list).\n"
                            + "  - aspiration: (integer) the aspiration criteris.\n\n"
                            + "For the Genetic Algorithm, the parameters are:\n\n"
                            + "  - population_size: (integer) the size of the population.\n"
                            + "  - generations: (integer) the number of generations.\n"
                            + "  - mutation_rate: (float, 0.0-1.0) the mutation rate.\n\n"
                            + "The input file will contain the list of ingredients that each client likes and dislikes.\n\n" 
                            + "The solution will contain the list of ingredients that should be included in the pizza.\n\n" 
                            + "The score will be the number of clients that will come to your pizzeria.\n\n" 
                            + "The output will contain the progress of the algorithm (each iteration).\n\n" 
                            + "The elapsed time will be the time it took to run the algorithm.\n\n" 
                            + "The clear button will clear the output, solution and score.\n\n" 
                            + "The run button will run the algorithm.\n\n" 
                            + "The option menu will allow you to select the file and the algorithm.\n\n" 
                            + "The appearance mode option menu will allow you to select the appearance mode.\n\n" 
                            + "The UI scaling option menu will allow you to select the UI scaling.\n\n"
                            + "The parameters button will allow you to type in parameters.\n\n"
                            + "The correct syntax for the parameters is: <parameter_name>=<parameter_value>.\n\n"    
                            )
        self.output.insert("0.0", "Output\n\n")
        self.solution.insert("0.0", "Solution\n\nThe solution will be shown here.\nIt will be a list of ingredients that should be included in the pizza.\n\n")
        self.progress_bar.configure(mode="indeterminnate")
        self.progress_bar.start()

    ### Event Handlers ###
        
    # Set the file to be used
    def option_file_callback(self, choice):
        print("Selected File:", choice)
        choice_idx = ["Example", "Basic", "Coarse", "Dificult", "Elaborate"].index(choice)
        self.set_file(choice=choice_idx)

    # Set the algorithm to be used
    def option_algorthim_callback(self, choice):
        print("Selected Algorithm:", choice)
        choice_idx = ["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"].index(choice)
        self.set_algorithm(choice=choice_idx)

    # Get the parameters from the user
    def param_button_callback(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a parameter (view instructions for further details):", title="Paramemters")
        parameters = dialog.get_input().split(",")  # Split the parameters by comma
        # remove white spaces
        parameters = [param.strip() for param in parameters]
        parameters = {param.split("=")[0]: param.split("=")[1] for param in parameters}  # Create a dictionary from the parameters
        self.set_parameters(parameters)
        print("Parameters:", parameters)

    # Run the algorithm
    def run_button_callback(self):
        self.progress_bar.start()
        start = time.perf_counter()
        solution, score = self.start_algorithm(self.update_solution_and_score, self.insert_output)
        end = time.perf_counter()
        # Elapsed time in seconds with 2 decimal places
        elapsed_time = "{:.2f} s".format(end - start)
        self.time.configure(text=elapsed_time)
        self.update_solution_and_score(solution, score)
        self.insert_output("Algorithm finished.\n")
        self.progress_bar.stop()

    # Update the displayed solution and score
    def update_solution_and_score(self, solution, score):
        self.solution.delete("0.0", "end") # delete all text
        self.solution.insert("0.0", solution) # insert at line 0 character 0
        self.score.configure(text=score)
        self.solution_frame.update()

    # Insert output to the output textbox
    def insert_output(self, output):
        self.output.insert("end", output) # insert at line 0 character 0
        self.output.update()
    
    # Clear all textboxes
    def clear(self):
        self.output.delete("0.0", "end")
        self.output.insert("0.0", "Output\n\n")
        self.solution.delete("0.0", "end")
        self.solution.insert("0.0", "Solution\n\nThe solution will be shown here.\nIt will be a list of ingredients that should be included in the pizza.\n\n")
        self.score.configure(text="The Score")
        self.time.configure(text="0.0 s")

    # Change the appearance mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Change the UI scaling
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


def run_app(start_algorithm, set_file, set_algorithm, set_parameters):
    app = App(start_algorithm, set_file, set_algorithm, set_parameters)
    app.mainloop()