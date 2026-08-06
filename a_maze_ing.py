import sys

from mazegen.config import (ConfigError, load_config)
from mazegen.generator import MazeGenerator
from mazegen.validator import MazeValidator
from mazegen.solver import MazeSolver
from mazegen.hex_exporter import HexExporter
from vizualization.ascii_renderer import MazeRenderer

def main() -> int:

    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py config.txt")
            return 1
        
        config = load_config(sys.argv[1])

        generator = MazeGenerator(
            width = config.width,
            height = config.height,
            seed = config.seed,
        )

        generator.generate()

        maze = generator.get_maze()
        validator = MazeValidator(maze)

        if not validator.validate():
            print("Generated maze is invalid.")
            return 1

        solver = MazeSolver(maze)

        path = solver.solve(config.entry, config.exit,)

        path_string = (solver.path_to_directions(path))

        exporter = HexExporter()

        exporter.write(
            maze=maze,
            output_file=config.output_file,
            entry=config.entry,
            exit=config.exit,
            path=path_string,
        )

        renderer = MazeRenderer(maze)

        renderer.interactive_view(
            config.entry,
            config.exit,
            path,
        )
        return 0
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
