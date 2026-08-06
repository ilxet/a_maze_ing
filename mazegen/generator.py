import random

from mazegen.models import Position, Cell

class MazeGenerator:

    def __init__(
            self, 
            width: int, 
            height: int, 
            seed: int | None = None,
            ) -> None:
        self.width = width
        self.height = height

        self.random = random.Random(seed)

        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

    def get_cell(self, position: Position) -> Cell:
        return self.grid[position.y][position.x]

    def is_inside(self, position: Position) -> bool:
        return (
        0 <= position.x < self.width
        and 0 <= position.y < self.height
    )

    def get_unvisited_neighbors(self, position: Position) -> list[Position]:
        directions = [
        (0, -1),  # north
        (1, 0),   # east
        (0, 1),   # south
        (-1, 0),  # west
        ]
        neighbors: list[Position] = []

        for dx, dy in directions:
            neighbor = Position(position.x + dx, position.y + dy)

            if not self.is_inside(neighbor):
                continue

            neighbor_cell = self.get_cell(neighbor)

            if neighbor_cell.blocked:
                continue

            if neighbor_cell.visited:
                continue

            neighbors.append(neighbor)

        return neighbors

    def remove_wall(self, current: Position, neighbor: Position) -> None:
        current_cell = self.get_cell(current)
        neighbor_cell = self.get_cell(neighbor)

        dx = neighbor.x - current.x
        dy = neighbor.y - current.y

        if dx == 0 and dy == -1:
            current_cell.north = False
            neighbor_cell.south = False

        elif dx == 1 and dy == 0:
            current_cell.east = False
            neighbor_cell.west = False

        elif dx == 0 and dy == 1:
            current_cell.south = False
            neighbor_cell.north = False

        elif dx == -1 and dy == 0:
            current_cell.west = False
            neighbor_cell.east = False

        else:
            raise ValueError("Cells are not adjacent")

    def generate(self) -> None:
        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        while True:
            start = Position(
                self.random.randrange(self.width),
                self.random.randrange(self.height),
            )

            if not self.get_cell(start).blocked:
                break

        stack: list[Position] = [start]

        self.get_cell(start).visited = True

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                neighbor = self.random.choice(neighbors)
                self.remove_wall(current, neighbor)
                self.get_cell(neighbor).visited = True
                stack.append(neighbor)
            else:
                stack.pop()

        self.reset_visited()

    def reset_visited(self) -> None:

        for row in self.grid:
            for cell in row:
                cell.visited = False

    def get_maze(self) -> list[list[Cell]]:
        return self.grid

