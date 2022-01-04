import pygame
import random
import copy as cp
from pprint import pprint as pp
from pygame.locals import *
from pygame.sndarray import array

Cell = tuple[int, int]
Cells = list
Grid = list[list[int]]

class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=5) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid: Grid = []

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        """
        if randomize:
            return [[random.randint(0,1) for j in range(self.cell_width)] for i in range(self.cell_height)]
        else: 
            return [[0 for j in range(self.cell_width)] for i in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.

        """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                if self.grid[y][x] == 1:
                    color = pygame.Color('green')
                elif self.grid[y][x] == 0:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: tuple) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        """
        neighs = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (cell[0]+a < 0) or (cell[0]+a >= self.cell_height) or (cell[1]+b < 0) or (cell[1]+b >= self.cell_width) or (a == b == 0): continue
                y_bound, x_bound = cell[0]+a, cell[1]+b
                if (y_bound >= 0) and (y_bound < self.cell_height) and (x_bound >= 0) and (x_bound < self.cell_width):
                    if self.grid[y_bound][x_bound] == 1: neighs.append([y_bound, x_bound])
        return neighs

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        newgen = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                cell = (y, x)
                if self.grid[y][x] == 1 and (len(self.get_neighbours(cell)) == 2 or len(self.get_neighbours(cell)) == 3):
                    newgen.append([y, x])
                elif self.grid[y][x] == 0 and len(self.get_neighbours(cell)) == 3:
                    newgen.append([y, x])

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if [y, x] in newgen: self.grid[y][x] = 1
                else: self.grid[y][x] = 0

        return self.grid


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

def main():
    game = GameOfLife(1280, 720, 10)
    #game = GameOfLife(320, 240, 40)
    game.run() 

if __name__ == '__main__':
    main()
