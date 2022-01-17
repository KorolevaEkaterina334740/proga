from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord[0], coord[1]
    grid[x][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    choose = ["up", "right"]
    for i in range(len(grid) - 2, 0, -2):
        for j in range(1, len(grid[0]) - 1, 2):
            if i == 1 and j == len(grid) - 2:
                break
            coordinate = choice(choose)
            if coordinate == "up":
                if i == 1:
                    remove_wall(grid, (i, j + 1))
                else:
                    remove_wall(grid, (i - 1, j))
            else:
                if j == len(grid) - 2:
                    remove_wall(grid, (i - 1, j))
                else:
                    remove_wall(grid, (i, j + 1))

    # генерация входа и выхода

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    chances = []
    outs = []
    for i in range(0, len(grid)):
        chances.append([0, i])
        chances.append([i, 0])
        chances.append([len(grid) - 1, i])
        chances.append([i, len(grid) - 1])
    for j in range(len(chances)):
        x, y = chances[j][0], chances[j][1]
        if grid[x][y] == "X" and (x, y) not in outs:
            outs.append((x, y))
    return outs


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    cells = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == k:
                cells.append([i, j])
    for a in range(len(cells)):
        x, y = cells[a][0], cells[a][1]
        if (y != 0 and grid[x][y - 1] == " ") or (y != 0 and grid[x][y - 1] == 0):
            grid[x][y - 1] = k + 1
        if (x != 0 and grid[x - 1][y] == " ") or (x != 0 and grid[x - 1][y] == 0):
            grid[x - 1][y] = k + 1
        if (y != len(grid) - 1 and grid[x][y + 1] == " ") or (y != len(grid) - 1 and grid[x][y + 1] == 0):
            grid[x][y + 1] = k + 1
        if (x != len(grid) - 1 and grid[x + 1][y] == " ") or (x != len(grid) - 1 and grid[x + 1][y] == 0):
            grid[x + 1][y] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    a, b = exit_coord[0], exit_coord[1]
    ex = grid[a][b]
    k = grid[a][b] - 1
    list = []
    temp = a, b
    list.append(temp)
    while k != 0:
        if a + 1 < len(grid):
            if grid[a + 1][b] == k:
                temp = a + 1, b
                a += 1
        if a - 1 >= 0:
            if grid[a - 1][b] == k:
                temp = a - 1, b
                a -= 1
        if b + 1 < len(grid):
            if grid[a][b + 1] == k:
                temp = a, b + 1
                b += 1
        if b - 1 >= 0:
            if grid[a][b - 1] == k:
                temp = a, b - 1
                b -= 1
        list.append(temp)
        k -= 1
    if len(list) != ex:
        x, y = list[-1][0], list[-1][1]
        grid[x][y] = " "
        c, d = list[-2][0], list[-2][1]
        shortest_path(grid, (c, d))
    return grid, list


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]
    if (x == 0 and y == 0) or (x == 0 and y == len(grid) - 1) or (x == len(grid) - 1 and y == 0) or (x == len(grid) - 1 and y == len(grid)) or (y == 0 and grid[x][y + 1] == "■") or (y == len(grid) - 1 and grid[x][y - 1] == "■") or (x == 0 and grid[x + 1][y] == "■") or (x == len(grid) - 1 and grid[x - 1][y] == "■"):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    outs = get_exits(grid)
    if len(outs) != 2:
        return None
    x, y = outs[0][0], outs[0][1]
    a, b = outs[1][0], outs[1][1]
    if encircled_exit(grid, (x, y)):
        return None
    if encircled_exit(grid, (a, b)):
        return None
    k = 1
    grid[x][y], grid[a][b] = 1, 0
    while grid[a][b] == 0:
        make_step(grid, k)
        k += 1
    grid, list = shortest_path(grid, (a, b))
    return grid, list


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                if str(grid[i][j]).isdigit():
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
