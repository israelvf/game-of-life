import sys, pygame
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
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.cell_skin = pygame.Surface((self.grid_size, self.grid_size))
        self.cell_skin.fill((255, 255, 255))
        self.initial_conditions()

    def initial_conditions(self):
        self.alive_cells = list()
        self.dead_cells = list()
        quantity = randint(1, 20)
        for i in range(0, quantity):
            cell_group = self.create_cell_group()
            self.alive_cells = [*self.alive_cells, *cell_group]
        for x in range(0, self.screen_width - self.grid_size, self.grid_size):
            for y in range(0, self.screen_height - self.grid_size, self.grid_size):
                if (x, y) not in self.alive_cells:
                    self.dead_cells.append((x, y))

    def create_cell_group(self):
        group_size = randint(1, 15)
        cells = self.initialize_cells(group_size)
        return cells

    def initialize_cells(self, size):
        cells = list()
        first_cell_position = self.on_grid_random()
        cells.append(first_cell_position)

        for i in range(0, size - 1):
            found_next_cell_position = False
            next_cell_position = (0, 0)
            while found_next_cell_position == False:
                next_cell_position = self.on_grid_adjacent(cells[i])
                if next_cell_position not in cells:
                    found_next_cell_position = True

            cells.append(next_cell_position)

        return cells

    def on_grid_random(self):
        x = randint(0, self.screen_width - self.grid_size)
        y = randint(0, self.screen_height - self.grid_size)

        return (x//self.grid_size * self.grid_size, y//self.grid_size * self.grid_size)

    def on_grid_adjacent(self, point):
        while True:
            xn = randint(-1, 1) * self.grid_size
            yn = randint(-1, 1) * self.grid_size

            valid_xn = xn >= 0 and xn < self.screen_width
            valid_yn = xn >= 0 and xn < self.screen_height

            if (xn != 0 and valid_xn) or (yn != 0 and valid_yn):
                return (point[0] + xn, point[1] + yn)

    def check_alive(self, position, current_state):
        alive_neighbors = self.check_neighborhood(position)
        if alive_neighbors < 2 or alive_neighbors > 3:
            return False
        elif alive_neighbors == 3:
            return True

        return current_state

    def check_neighborhood(self, position, radius=1):
        alive_cells = 0
        x_pos = position[0]
        y_pos = position[1]
        start = radius * self.grid_size
        stop = (radius * self.grid_size) + self.grid_size
        for x in range(x_pos - start, x_pos + stop, self.grid_size):
            for y in range(y_pos - start, y_pos + stop, self.grid_size):
                if x == x_pos and y == y_pos:
                    continue
                if (x, y) in self.alive_cells:
                    alive_cells += 1

        return alive_cells

    def remove_out_of_grid_cells(self):
        for cell in self.alive_cells:
            if cell[0] < 0 or cell[0] > self.screen_width or cell[1] < 0 or cell[1] > self.screen_height:
                self.alive_cells.remove(cell)

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
        iteration_alive_cells = list()
        iteration_dead_cells = list()
        for cell in self.alive_cells:
            still_alive = self.check_alive(cell, True)
            if still_alive:
                iteration_alive_cells.append(cell)
            else:
                iteration_dead_cells.append(cell)
        for cell in self.dead_cells:
            still_dead = not self.check_alive(cell, False)
            if still_dead:
                iteration_dead_cells.append(cell)
            else:
                iteration_alive_cells.append(cell)

        self.alive_cells = iteration_alive_cells
        self.dead_cells = iteration_dead_cells

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    def render_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.update_fps(), (10, 0))
        for pos in self.alive_cells:
            self.screen.blit(self.cell_skin, pos)

        pygame.display.update()

    def run(self):
        self.remove_out_of_grid_cells()
        self.update_clock_tick()
        self.process_game_events()
        if not self.pause:
            self.process_game_rules()
        self.render_screen()
        pygame.time.wait(500)

if __name__ == "__main__":
    game = GameOfLife()
    while True:
        game.run()
