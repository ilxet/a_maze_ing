from collections import deque

from mazegen.models import Cell, Position


class MazeSolver:
    # finds shortest path in the maze yo >_<

    def __init__(self, maze: list[list[Cell]]) -> None:

        self.maze = maze

        self.height = len(maze)
        self.width = (len(maze[0]) if maze else 0)

    def get_cell(self, position: Position) -> Cell:

        return self.maze[position.y][position.x]

    def is_inside(self, position: Position) -> bool:

        return (
            0 <= position.x < self.width
            and
            0 <= position.y < self.height
        )

    def get_neighbors(self, position: Position) -> list[Position]:
    
        cell = self.get_cell(position)
        neighbors: list[Position] = []

        if not cell.north:
            neighbors.append(Position(position.x, position.y - 1))

        if not cell.east:
            neighbors.append(Position(position.x + 1, position.y))

        if not cell.south:
            neighbors.append(Position(position.x, position.y + 1))

        if not cell.west:
            neighbors.append(Position(position.x - 1, position.y))

        return [
            neighbor
            for neighbor in neighbors
            if self.is_inside(neighbor)
        ]

    def solve(self, start: Position, goal: Position) -> list[Position]:

        queue = deque([start])
        visited: set[Position] = {start}
        parents: dict[Position, Position | None] = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

        if goal not in parents:
            return []

        path: list[Position] = []
        path_position: Position | None = goal

        while path_position is not None:
            path.append(path_position)
            path_position = parents[path_position]
        path.reverse()
        return path

    def path_to_directions(self, path: list[Position]) -> str:

        if len(path) < 2:
            return ""
        directions: list[str] = []
        for current, nxt in zip(path, path[1:]):
            dx = nxt.x - current.x
            dy = nxt.y - current.y
            if dx == 0 and dy == -1:
                directions.append("N")
            elif dx == 1 and dy == 0:
                directions.append("E")
            elif dx == 0 and dy == 1:
                directions.append("S")
            elif dx == -1 and dy == 0:
                directions.append("W")
        return "".join(directions)
    