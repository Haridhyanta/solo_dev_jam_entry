from dataclasses import dataclass
import json

from color import Color, CHAR_TO_ENUM_COLOR
from rule import NAME_TO_RULE


@dataclass
class LevelInfo:
    name: str
    solution_grid: list[list[Color]]
    color_options: list[Color]
    color_no_left: list[int]
    rules: list[type]

def load_level(level_no: int) -> LevelInfo:
    FILE_PATH: str = f'./levels/level_{level_no}.json'
    
    try:
        with open(FILE_PATH, "r") as file:
            loaded_data = json.load(file)
            name: str = loaded_data["name"]
            level_strings: list[str] = loaded_data["solution"]
            solution_grid: list[list[Color]] = []
            for level_string in level_strings:
                current_row: list[Color] = []
                for ch in level_string:
                    current_row.append(CHAR_TO_ENUM_COLOR[ch])
                
                solution_grid.append(current_row)
            
            color_options: list[Color] = list(map(lambda x: CHAR_TO_ENUM_COLOR[x], loaded_data["color_options"]))
            
            color_no_left = loaded_data["color_no_left"]

            rules: list[type] = list(map(lambda x: NAME_TO_RULE[x], loaded_data["rules"]))

            return LevelInfo(
                name,
                solution_grid,
                color_options,
                color_no_left,
                rules
            )

    except FileNotFoundError:
        raise ValueError(f"Level number '{level_no}' not found")
