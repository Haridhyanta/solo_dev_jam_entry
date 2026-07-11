import enum

from pygame import Color as PygameColor

class Color(enum.IntEnum):
    BLACK = enum.auto()
    RED = enum.auto()
    GREEN = enum.auto()

enum_to_color: list[PygameColor] = [
    PygameColor("Black"), # Should not be accessed
    PygameColor("Black"),
    PygameColor("Red"),
    PygameColor("Green"),
]
