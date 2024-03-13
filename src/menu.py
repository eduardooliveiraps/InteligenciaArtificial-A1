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

    def start(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    # Handle any input events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if self.current_state == MenuState.MENU:
                    self.handle_menu_input(event.key)
                elif self.current_state == MenuState.LOADING:
                    self.handle_gameplay_input(event.key)
                elif self.current_state == MenuState.RESULTS:
                    self.handle_results_input(event.key)

    # Handle input events in the MENU state
    def handle_menu_input(self, key):
        if key == pygame.K_1:  # start gameplay
            self.current_state = MenuState.LOADING
        elif key == pygame.K_2:  # quit game
            self.quit_game()

    # Handle input events in the LOADING state
    def handle_gameplay_input(self, key):
        if key == pygame.K_p:  # pause
            self.current_state = MenuState.RESULTS

    # Handle quit input events
    def handle_quit_input(self, key):
        if key == pygame.K_q:  # quit game
            self.quit_game()

    # Handle input events in the RESULTS state
    def handle_results_input(self, key):
        if key == pygame.K_r:  # restart game
            self.current_state = MenuState.MENU

    # Update the game state
    def update(self):
        if self.current_state == MenuState.MENU:
            # game logic and update here
            pass

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
        # render menu here
        menu = pygame_menu.Menu('Welcome', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)

        menu.add.dropselect('File :', [('Example', 0), ('Basic', 1), ('Coarse', 2), ('Dificult', 3), ('Elaborate', 4)], onchange=self.set_file)
        menu.add.dropselect('Algorithm :', [('Hill Climbing', 0), ('Simulated Annealing', 1), ('Tabu Search', 2), ('Genetic Algorithm', 3)], onchange=self.set_algorithm)
        menu.add.button('Run', self.start_algorithm)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    # Render the gameplay screen
    def render_loading(self):
        # render gameplay here
        pass

    # Render the game over screen
    def render_results(self):
        # render results over here
        menu = pygame_menu.Menu('Solution', 1000, 700,
                        theme=pygame_menu.themes.THEME_DARK)
        menu.add.label(f"Best solution: {solution}")
        menu.add.label(f"Score: {score}")
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.screen)

    # Quit the game
    def quit_game(self):
        pygame.quit()
        quit()


# Entry point of the program
if __name__ == "__main__":
    game_state_manager = MenuStateManager()
    game_state_manager.start()