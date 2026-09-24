import enum

from pygame import Color as PygameColor

class Color(enum.IntEnum):
    VIOLET = enum.auto()
    INDIGO = enum.auto()
    BLUE = enum.auto()
    GREEN = enum.auto()
    ORANGE = enum.auto()
    YELLOW = enum.auto()
    RED = enum.auto()
    BLACK = enum.auto()
    WHITE = enum.auto()

enum_to_color: list[PygameColor] = [
    PygameColor(0, 0, 0, 0), # Should not be accessed
    PygameColor("Violet"),
    PygameColor("Indigo"),
    PygameColor(33, 165, 213),
    PygameColor("Green"),
    PygameColor("Orange"),
    PygameColor("Yellow"),
    PygameColor("Red"),
    PygameColor("Black"),
    PygameColor("White"),
]

CHAR_TO_ENUM_COLOR: dict[str, Color] = {
    'V': Color.VIOLET,
    'I': Color.INDIGO,
    'B': Color.BLUE,
    'G': Color.GREEN,
    'Y': Color.YELLOW,
    'O': Color.ORANGE,
    'R': Color.RED,
    'W': Color.WHITE,
    '0': Color.BLACK,
    'P': Color.VIOLET, # Here for "compatibility reason"
}