from collections import deque

from mazegen.models import Cell, Position


class MazeValidator:
    def __init__(self, maze: list[list[Cell]]) -> None:
        self.maze = maze

        self.height = len(maze)

        self.width = (len(maze[0]) if maze else 0)

    def get_cell(self, position: Position) -> Cell:
        # return maze cell
        return self.maze[position.y][position.x]

    def is_inside(self, position: Position) -> bool:
        # checks bounds
        return (
            0 <= position.x < self.width
            and
            0 <= position.y < self.height
        )

    def check_wall_consistency(self) -> bool:
        # checking and verifyng if neighbor walls are fine
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                cell = self.get_cell(position)
                if x < self.width - 1:
                    neighbor = self.get_cell(Position(x + 1, y))
                    if cell.east != neighbor.west:
                        return False

                if y < self.height - 1:
                    neighbor = self.get_cell(Position(x, y + 1))
                    if cell.south != neighbor.north:
                        return False
        return True

    def check_connectivity(self) -> bool:
        start: Position | None = None

        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)

                if not self.get_cell(position).blocked:
                    start = position
                    break
            if start is not None:
                break
        if start is None:
            return False
        visited: set[Position] = {start}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            cell = self.get_cell(current)
            neighbors: list[Position] = []
            if not cell.north and current.y > 0:
                neighbors.append(Position(current.x, current.y - 1,))
            if not cell.east and current.x < self.width - 1:
                neighbors.append(Position(current.x + 1, current.y))
            if not cell.south and current.y < self.height - 1:
                neighbors.append(Position(current.x, current.y + 1))
            if not cell.west and current.x > 0:
                neighbors.append(Position(current.x - 1, current.y))
            for neighbor in neighbors:
                if self.get_cell(neighbor).blocked:
                    continue
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(neighbor)

        reachable_cells = sum(
            1
            for row in self.maze
            for cell in row
            if not cell.blocked
        )

        return len(visited) == reachable_cells

    def validate(self) -> bool:
        # runs all validations checks
        if not self.check_wall_consistency():
            return False
        if not self.check_connectivity():
            return False
        return True