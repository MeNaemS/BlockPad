from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(slots=True)
class Dotenv:
    config_path: str
    config_file: str
    shapes_path: str


@dataclass(slots=True)
class ColorsOfShapes:
    green: Dict[str, List[Tuple[int, int, int]]]
    orange: Dict[str, List[Tuple[int, int, int]]]
    red: Dict[str, List[Tuple[int, int, int]]]
    cyan: Dict[str, List[Tuple[int, int, int]]]
    gold: Dict[str, List[Tuple[int, int, int]]]


@dataclass(slots=True)
class WindowSettings:
    size: tuple[int, int]


@dataclass(slots=True)
class Config:
    colors: ColorsOfShapes
    shapes: List[str]
    window: WindowSettings
    background_menu_path: str
    background_game_path: str
