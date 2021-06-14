import sys
import pygame
import numpy as np
from pygame.locals import *
from random import randint


class GameOfLife:

    def __init__(self):
        pygame.display.set_caption("Game of Life")
        pygame.init()
        pygame.mixer.quit()
        self.font = pygame.font.SysFont("Arial", 18)
        self.fps = 60
        self.pause = False
        self.screen_width = 600
        self.screen_height = 600
        self.grid_size = 10
        self.grid_x_size = int(self.screen_width / self.grid_size)
        self.grid_y_size = int(self.screen_height / self.grid_size)
        self.grid = np.zeros((self.grid_x_size, self.grid_y_size))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.cell_skin = pygame.Surface((self.grid_size, self.grid_size))
        self.cell_skin.fill((255, 255, 255))
        self.initial_conditions()

    def initial_conditions(self):
        self.grid = np.random.randint(2, size=(self.grid_x_size, self.grid_y_size))

    def on_grid_random(self):
        x = randint(0, self.screen_width - self.grid_size)
        y = randint(0, self.screen_height - self.grid_size)

        return (x//self.grid_size * self.grid_size, y//self.grid_size * self.grid_size)

    def check_alive(self, position, current_state):
        alive_neighbors = self.check_neighborhood(position)
        if alive_neighbors < 2 or alive_neighbors > 3:
            return 0
        elif alive_neighbors == 3:
            return 1

        return current_state

    def check_neighborhood(self, position, radius=1):
        filter_size = 2 * radius + 1
        filter_matrix = np.ones((filter_size, filter_size))
        filter_matrix[radius][radius] = 0

        alive_cells = 0

        for pos, filter_value in np.ndenumerate(filter_matrix):
            x = int((position[0] + (pos[0] - radius)) % self.grid_x_size)
            y = int((position[1] + (pos[1] - radius)) % self.grid_y_size)

            alive_cells += self.grid[x][y] * filter_value

        return alive_cells

    def update_clock_tick(self):
        self.clock.tick(self.fps)

    def process_game_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    pass
                if event.key == K_SPACE:
                    self.pause = not self.pause
                if event.key == K_RETURN:
                    self.initial_conditions()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def process_game_rules(self):
        iteration_cells = np.zeros((self.grid_x_size, self.grid_y_size))

        for position, cell_state in np.ndenumerate(self.grid):
            iteration_cells[position] = self.check_alive(position, cell_state)

        self.grid = iteration_cells

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    def render_screen(self):
        self.screen.fill((0, 0, 0))

        for position, cell_state in np.ndenumerate(self.grid):
            if cell_state:
                pos_x = position[0] * self.grid_size
                pos_y = position[1] * self.grid_size
                pos = (pos_x, pos_y)
                self.screen.blit(self.cell_skin, pos)

        self.screen.blit(self.update_fps(), (10, 0))

        pygame.display.update()

    def run(self):
        self.update_clock_tick()
        self.process_game_events()
        if not self.pause:
            self.process_game_rules()
        self.render_screen()


if __name__ == "__main__":
    game = GameOfLife()
    while True:
        game.run()
