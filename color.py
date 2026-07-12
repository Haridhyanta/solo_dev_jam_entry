import enum

from pygame import Color as PygameColor

class Color(enum.IntEnum):
    BLACK = enum.auto()
    RED = enum.auto()
    GREEN = enum.auto()
    WHITE = enum.auto()

enum_to_color: list[PygameColor] = [
    PygameColor("Black"), # Should not be accessed
    PygameColor("Black"),
    PygameColor("Red"),
    PygameColor("Green"),
    PygameColor("White"),
]

CHAR_TO_ENUM_COLOR: dict[str, Color] = {
    'B': Color.BLACK,
    'R': Color.RED,
    'G': Color.GREEN,
    'W': Color.WHITE,
}