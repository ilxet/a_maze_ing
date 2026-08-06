from mazegen.models import Cell, Position

class HexExporter:

    def cell_to_hex(self, cell: Cell) -> str:
        value = 0

        if cell.north:
            value |= 1

        if cell.east:
            value |= 2

        if cell.south:
            value |= 4

        if cell.west:
            value |= 8

        return format(value, "X")

    def write(
        self,
        maze: list[list[Cell]],
        output_file: str,
        entry: Position,
        exit: Position,
        path: str,
    ) -> None:
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                for row in maze:
                    line = "".join(self.cell_to_hex(cell) for cell in row)
                    file.write(f"{line}\n")
                file.write("\n")
                file.write(f"{entry.x},{entry.y}\n")
                file.write(f"{exit.x},{exit.y}\n")
                file.write(f"{path}\n")
        except OSError as exc:
            raise RuntimeError(f"Unable to write '{output_file}'") from exc
