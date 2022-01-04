import curses

from life_game_files import GameOfLife
from LG_ui import UI

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.rows = len(self.life.curr_generation)
        self.cols = len(self.life.curr_generation[0])

    def draw_borders(self, screen) -> None:
        screen.border()

    def draw_grid(self, screen) -> None:
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                symbol = "●" if self.life.curr_generation[i][j] else " "
                screen.addch(i + 1, j + 1, symbol)

    def run(self) -> None:
        curses.initscr()
        screen = curses.newwin(self.rows + 3, self.cols + 3, 0, 0)
        self.draw_borders(screen)

        try:
            while self.life.is_changing or not self.life.is_max_generations_exceeded:
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                self.life.step()
                curses.napms(750)#to have chance to notice the difference
        finally:
            curses.endwin()


def main():
    game = GameOfLife(size=(20, 45))
    app = Console(game)
    app.run()


if __name__ == "__main__":
    main()
