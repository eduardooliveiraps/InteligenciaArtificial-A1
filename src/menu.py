import pygame
import pygame_menu
from enum import Enum

# Define the possible game states using an Enum
class MenuState(Enum):
    MENU = 0
    LOADING = 1
    RESULTS = 2


# The MenuStateManager class manages the game states and handles events, updates, and rendering
class MenuStateManager:
    def __init__(self, start_algorithm, set_file, set_algorithm, width=1000, heigh=700):
        self.start_algorithm = start_algorithm
        self.set_file = set_file
        self.set_algorithm = set_algorithm

        pygame.init()
        self.screen = pygame.display.set_mode((width, heigh))
        pygame.display.set_caption("One Pizza")

        self.current_state = MenuState.MENU

    # Render the current state
    def render(self):
        self.screen.fill((0, 0, 0))  # clear screen

        if self.current_state == MenuState.MENU:
            self.render_initial_menu()
        elif self.current_state == MenuState.LOADING:
            self.render_loading()
        elif self.current_state == MenuState.RESULTS:
            self.render_results()

        pygame.display.flip()  # update screen

    # Render the menu screen
    def render_initial_menu(self):
        menu = pygame_menu.Menu('Welcome', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)

        menu.add.dropselect('File :', [('Example', 0), ('Basic', 1), ('Coarse', 2), ('Dificult', 3), ('Elaborate', 4)], onchange=self.set_file)
        menu.add.dropselect('Algorithm :', [('Hill Climbing', 0), ('Simulated Annealing', 1), ('Tabu Search', 2), ('Genetic Algorithm', 3)], onchange=self.set_algorithm)
        menu.add.button('Run', self.render_loading)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    # Render the gameplay screen
    def render_loading(self):
        solution, score = self.start_algorithm()
        self.render_results(solution, score)


    # Render the game over screen
    def render_results(self, solution, score):
        self.start_algorithm()
        menu = pygame_menu.Menu('Solution', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)
        menu.add.label(f"Best solution: {solution}")
        menu.add.label(f"Score: {score}")
        menu.add.button('Back', self.render_initial_menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    # Quit the game
    def quit_game(self):
        pygame.quit()
        quit()
