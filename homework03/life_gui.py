import pygame
from pygame.locals import *

import life_game_files as lgf 
from life_game_files import GameOfLife
from LG_ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        # ...
        super().__init__(life)
        self.height = self.life.rows * cell_size
        self.width = self.life.cols * cell_size
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed
    
    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.

        """
        for y in range(len(self.life.curr_generation)):
            for x in range(len(self.life.curr_generation[y])):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if self.life.curr_generation[y][x] == 1:
                    color = pygame.Color('green')
                elif self.life.curr_generation[y][x] == 0:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen, color, rect)

    def change_state(self, cell: lgf.Cell) -> None:
        yc_crd = cell[0] // self.cell_size
        xc_crd = cell[1] // self.cell_size
        if self.life.curr_generation[yc_crd][xc_crd]:
            self.life.curr_generation[yc_crd][xc_crd] = 0
        else:
            self.life.curr_generation[yc_crd][xc_crd] = 1

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.life.curr_generation = self.life.create_grid(randomize=True)
        running = True
        pause = False
        while running:
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (x_crd, y_crd) = (pygame.mouse.get_pos())
                    #neccessary to invert coordinates due to different matrix and get_pos() coord-systems 
                    self.change_state((y_crd, x_crd)) 
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)
                    continue
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE:  
                        if pause:
                            pause = False
                        else:
                            pause = True
            if pause:  # game pause
                continue

            # Выполнение одного шага игры (обновление состояния ячеек)
            if self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()
                pygame.display.flip()
            else:
                running = False
            clock.tick(self.speed)
        pygame.quit()


def main():
    game = GameOfLife(size=(48, 64))
    app = GUI(game)
    app.run()

if __name__ == "__main__":
    main()
