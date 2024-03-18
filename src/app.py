import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, start_algorithm, set_file, set_algorithm, width=1280, heigh=720):
        super().__init__()
        self.start_algorithm = start_algorithm
        self.set_file = set_file
        self.set_algorithm = set_algorithm

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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="One Pizza", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.dev_label = customtkinter.CTkLabel(self.sidebar_frame, text="Developed by", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.dev_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.dev_name_1 = customtkinter.CTkLabel(self.sidebar_frame, text="Eduardo Oliveira", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.dev_name_1.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.dev_name_2 = customtkinter.CTkLabel(self.sidebar_frame, text="João Francisco Alves", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.dev_name_2.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.dev_name_3 = customtkinter.CTkLabel(self.sidebar_frame, text="José Miguel Isidro", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.dev_name_3.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(30, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox for One Pizza Problem
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create textbox for output
        self.output = customtkinter.CTkTextbox(self, width=250)
        self.output.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create options and progressbar frame
        self.options_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.options_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.optionmenu_file = customtkinter.CTkOptionMenu(self.options_frame,
                                                        command=self.option_file_callback,
                                                        values=["Example", "Basic", "Coarse", "Dificult", "Elaborate"])
        self.optionmenu_file.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_algorithm = customtkinter.CTkOptionMenu(self.options_frame,
                                                        command=self.option_algorthim_callback,
                                                        values=["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"])
        self.optionmenu_algorithm.grid(row=0, column=1, padx=20, pady=(20, 10))
        self.run_button = customtkinter.CTkButton(self.options_frame, text="Run",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                                                        command=self.run_button_callback)
        self.run_button.grid(row=1, column=1, padx=20, pady=(50, 10), sticky="ew")
        self.clear_button = customtkinter.CTkButton(self.options_frame, text="Clear Output",
                                                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                                                        command=self.clear_output)
        self.clear_button.grid(row=0, column=2, padx=20, pady=(20, 10), sticky="ew")
        self.progress_bar = customtkinter.CTkProgressBar(self.options_frame)
        self.progress_bar.grid(row=2, column=1, padx=20, pady=(50, 10), sticky="ew")
        self.solution_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.solution_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.solution_label = customtkinter.CTkLabel(self.solution_frame, text="Solution:", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.solution_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.solution = customtkinter.CTkTextbox(self.solution_frame, width=300, font=customtkinter.CTkFont(size=14, weight="normal"))
        self.solution.grid(row=0, column=1, padx=20, pady=(10, 10), sticky="ew")
        self.score_label = customtkinter.CTkLabel(self.solution_frame, text="Score:", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.score_label.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.score = customtkinter.CTkLabel(self.solution_frame, text="The score", font=customtkinter.CTkFont(size=14, weight="normal"))
        self.score.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="ew")

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_file.set("Select File")
        self.optionmenu_algorithm.set("Select Algorithm")
        self.textbox.insert("0.0", "One Pizza Problem\n\n" + "You are opening a small pizzeria. In fact, your pizzeria is so small that you decided to offer only one type of pizza.\nNow you need to decide what ingredients to include (peppers? tomatoes?both?).\nEveryone has their own pizza preferences.\nEach of your potential clients has some ingredientsthey like, and maybe some ingredients they dislike.\nEach client will come to your pizzeria if both conditions are true:\n\n  1. all the ingredients they like are on the pizza\n  2. none of the ingredients they dislike are on the pizza.\n\n")
        self.output.insert("0.0", "Output\n\n")
        self.solution.insert("0.0", "Solution\n\nThe solution will be shown here.\nIt will be a list of ingredients that should be included in the pizza.\n\n")
        self.progress_bar.configure(mode="indeterminnate")
        self.progress_bar.start()

    def option_file_callback(self, choice):
        print("Selected File:", choice)
        choice_idx = ["Example", "Basic", "Coarse", "Dificult", "Elaborate"].index(choice)
        self.set_file(choice=choice_idx)

    def option_algorthim_callback(self, choice):
        print("Selected Algorithm:", choice)
        choice_idx = ["Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm"].index(choice)
        self.set_algorithm(choice=choice_idx)

    def run_button_callback(self):
        self.progress_bar.start()
        solution, score = self.start_algorithm(self.update_solution_and_score, self.insert_output)
        self.update_solution_and_score(solution, score)
        self.insert_output("Algorithm finished.\n")
        self.progress_bar.stop()

    def update_solution_and_score(self, solution, score):
        self.solution.delete("0.0", "end") # delete all text
        self.solution.insert("0.0", solution) # insert at line 0 character 0
        self.score.configure(text=score)
        self.solution_frame.update()

    def insert_output(self, output):
        self.output.insert("end", output) # insert at line 0 character 0
        self.output.update()
    
    def clear_output(self):
        self.output.delete("0.0", "end")
        self.output.insert("0.0", "Output\n\n")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


def run_app(start_algorithm, set_file, set_algorithm):
    app = App(start_algorithm, set_file, set_algorithm)
    app.mainloop()