import enum

from pygame import Color as PygameColor

class Color(enum.IntEnum):
    BLACK = enum.auto()
    RED = enum.auto()
    GREEN = enum.auto()
    WHITE = enum.auto()
    BLUE = enum.auto()
    PURPLE = enum.auto()

enum_to_color: list[PygameColor] = [
    PygameColor("Black"), # Should not be accessed
    PygameColor("Black"),
    PygameColor("Red"),
    PygameColor("Green"),
    PygameColor("White"),
    PygameColor("Blue"),
    PygameColor("Purple"),
]

CHAR_TO_ENUM_COLOR: dict[str, Color] = {
    '0': Color.BLACK,
    'R': Color.RED,
    'G': Color.GREEN,
    'W': Color.WHITE,
    'B': Color.BLUE,
    'P': Color.PURPLE,
}