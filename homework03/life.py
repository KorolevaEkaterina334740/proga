import json
import random
import pathlib
import copy as cp
from pprint import pprint as pp

Cell = tuple[int, int]
Cells = list
Grid = list[list[int]]


class GameOfLife:

    def __init__(self, size: tuple[int, int], randomize: bool=True, max_generations: int=None) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1


    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        """
        if randomize:
            return [[random.randint(0,1) for j in range(self.cols)] for i in range(self.rows)]
        else: 
            return [[0 for j in range(self.cols)] for i in range(self.rows)]


    def get_neighbours(self, cell: tuple) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        """
        neighs = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (cell[0]+a < 0) or (cell[0]+a >= self.rows) or (cell[1]+b < 0) or (cell[1]+b >= self.cols) or (a == b == 0): continue
                y_bound, x_bound = cell[0]+a, cell[1]+b
                if (y_bound >= 0) and (y_bound < self.rows) and (x_bound >= 0) and (x_bound < self.cols):
                    if self.curr_generation[y_bound][x_bound] == 1: neighs.append([y_bound, x_bound])
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
        next = cp.deepcopy(self.curr_generation)
        for y in range(len(self.curr_generation)):
            for x in range(len(self.curr_generation[y])):
                cell = (y, x)
                if self.curr_generation[y][x] == 1 and (len(self.get_neighbours(cell)) == 2 or len(self.get_neighbours(cell)) == 3):
                    newgen.append([y, x])
                elif self.curr_generation[y][x] == 0 and len(self.get_neighbours(cell)) == 3:
                    newgen.append([y, x])

        for y in range(len(next)):
            for x in range(len(next[y])):
                if [y, x] in newgen: next[y][x] = 1
                else: next[y][x] = 0

        return next


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = cp.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if (self.max_generations == None): return False
        else: return  self.generations > self.max_generations


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife": #better to use full pathname
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            saved_data = json.load(f)
        size = (len(saved_data), len(saved_data[0]))
        game = GameOfLife(size=size, randomize=False)
        game.curr_generation = saved_data
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            json.dump(self.curr_generation, fp=f)
        print("Data was saved in {}".format(pathlib.Path(filename).absolute()))
        pass

def main():
    filename = "gen{}.txt"

    def gen_path(step):
        return pathlib.Path(filename.format(step)).absolute()

    # New game
    game = GameOfLife(size=(10, 10))
    game.save(gen_path("_start")) #file to save start data

    #making steps
    game.step()
    game.save(gen_path(1))

    # loading game from save *and save again 😎*
    game = GameOfLife.from_file(gen_path(1))
    game.step()
    game.save(gen_path(2))


if __name__ == "__main__":
    main()
