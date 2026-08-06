from dataclasses import dataclass
from pathlib import Path

from mazegen.models import Position

@dataclass
class MazeConfig:

    width: int
    height: int
    entry: Position
    exit: Position
    output_file: str
    perfect: bool
    seed: int | None = None

class ConfigError(Exception):

    pass

def parse_position(pos: str) -> Position:

    try:
        x, y = pos.split(",", maxsplit = 1)
        return Position(int(x), int(y))
    except ValueError as exc:
        raise ConfigError(f"Invalid format of position in config file'{pos}'") from exc

def parse_bool(word: str) -> bool:

    if(word.lower() == "true"):
        return True
    
    elif(word.lower == "false"):
        return False
    
    else:
        raise ConfigError("Value for perfect in config file should be True or False")
 
    
def validate_maze(config: MazeConfig) -> None:

    if config.height < 0:
        raise ConfigError("Height must be greater than 0")

    if config.width < 0:
        raise ConfigError("Width must be greater than 0")

    if not ((0 <= config.entry.x <= config.width) or not (0 <= config.entry.y <= config.height)):
        raise ConfigError("Entry must be inside the maze")

    if not ((0 <= config.exit.x <= config.width) or not (0 <= config.exit.y <= config.height)):
        raise ConfigError("Exit must be inside the maze")

def load_config(path: str) -> MazeConfig:
    config_path = Path(path)

    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    config_data: dict[str, str] = {}

    try:
        with config_path.open("r", encoding = "utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ConfigError(f"Invalid line:'{line}'")

                key, value = line.split('=', maxsplit = 1)

                config_data[key.strip()] = value.strip()

    except OSError as exc:
        raise ConfigError(f"Unable to read configuration {path}") from exc

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }

    missing = required_keys - set(config_data)

    if missing:
        raise ConfigError(f"Missing config values:" + ", ".join(sorted(missing)))

    try:
        width = int(config_data["WIDTH"])
        height = int(config_data["HEIGHT"])
    except ValueError as exc:
        raise ConfigError("WIDTH and HEIGHT must be of type integer") from exc

    seed: int | None = None
    if "SEED" in config_data:
        try:
            seed = int(config_data["SEED"])
        except ValueError as exc:
            raise ConfigError("SEED must be of of type integer") from exc

    config = MazeConfig(
        width = width,
        height = height,
        entry = parse_position(config_data["ENTRY"]),
        exit = parse_position(config_data["EXIT"]),
        output_file = config_data["OUTPUT_FILE"],
        perfect = parse_bool(config_data["PERFECT"]),
        seed = seed,
    )

    validate_maze(config)

    return config
    


