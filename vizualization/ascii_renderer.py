from mazegen.models import Cell, Position
import os

WALL_COLORS = {
    "blue": "\033[34m",
    "green": "\033[32m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
}

RESET = "\033[0m"


class MazeRenderer:

    def __init__(self, maze: list[list[Cell]]) -> None:
        self.maze = maze
        self.wall_color = "blue"

    def set_wall_color(self, color: str) -> None:
        if color in WALL_COLORS:
            self.wall_color = color

    def render(
        self,
        entry: Position,
        exit: Position,
        path: list[Position] | None = None,
    ) -> None:
        color = WALL_COLORS[self.wall_color]
        if not self.maze:
            return

        path_set: set[Position] = set(path or [])

        print(color + "+" + "---+" * len(self.maze[0]) + RESET)

        for y, row in enumerate(self.maze):
            line = color + "|" + RESET
            bottom =color + "+"
            for x, cell in enumerate(row):
                position = Position(x, y)
                if cell.blocked:
                    char = "#"
                elif position == entry:
                    char = "E"
                elif position == exit:
                    char = "X"
                elif position in path_set:
                    char = "."
                else:
                    char = " "
                line += f" {char} "

                if cell.east:
                    line += color + "|" + RESET
                else:
                    line += " "

                if cell.south:
                    bottom += color + "---+" + RESET
                else:
                    bottom += "   " + color + "+" + RESET
            print(line)
            print(bottom)

    def interactive_view(
        self,
        entry: Position,
        exit: Position,
        path: list[Position],
    ) -> None:
        show_path = False
        while True:
            os.system("clear")
            self.render(entry, exit, path if show_path else None)
            print()
            print("[P] Toggle path")
            print("[C] Change color")
            print("[Q] Quit")

            choice = input("> ").strip().lower()
            if choice == "p":
                show_path = not show_path
            elif choice == "c":
                print()
                print("Available colors:")

                for color in WALL_COLORS:
                    print(f" - {color}")
                selected = input("> ").strip().lower()
                self.set_wall_color(selected)
            elif choice == "q":
                break
