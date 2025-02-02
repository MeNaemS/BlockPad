from dataclasses import dataclass


@dataclass(slots=True)
class Dotenv:
    config_path: str
    config_file: str
    shapes_path: str


@dataclass(slots=True)
class ColorsOfShapes:
    green: list[list[int]]
    orange: list[list[int]]
    red: list[list[int]]
    cyan: list[list[int]]
    gold: list[list[int]]


@dataclass(slots=True)
class WindowSettings:
    size: list[int, int]
    minimal_size: list[int, int]
    title: str


@dataclass(slots=True)
class GameSettings:
    FPS: int


@dataclass(slots=True)
class Config:
    colors: ColorsOfShapes
    shapes: list[str]
    window: WindowSettings
    game: GameSettings
    background_menu_path: str
    background_game_path: str
    icon: str
