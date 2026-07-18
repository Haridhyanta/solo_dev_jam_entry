import enum

from pygame import Rect, Surface

from game_data import GameData


class Direction(enum.Enum):
    RIGHT = enum.auto()
    UP = enum.auto()
    LEFT = enum.auto()
    DOWN = enum.auto()

    def next(self, pos: tuple[int, int], move_by: int=1) -> tuple[int, int]:
        match self:
            case Direction.RIGHT:
                return pos[0]+move_by, pos[1]
            case Direction.LEFT:
                return pos[0]-move_by, pos[1]
            case Direction.UP:
                return pos[0], pos[1]-move_by
            case Direction.DOWN:
                return pos[0], pos[1]+move_by

    def align_to_center(self, rect_to_move: Rect, fixed_rect: Rect) -> None:
        match self:
            case Direction.RIGHT:
                rect_to_move.center = fixed_rect.midright 
            case Direction.LEFT:
                rect_to_move.center = fixed_rect.midleft
            case Direction.UP:
                rect_to_move.center = fixed_rect.midtop
            case Direction.DOWN:
                rect_to_move.center = fixed_rect.midbottom

    def get_arrow(self, game_data: GameData) -> Surface:
        match self:
            case Direction.RIGHT:
                return game_data.right_arrow
            case Direction.LEFT:
                return game_data.left_arrow
            case Direction.UP:
                return game_data.up_arrow
            case Direction.DOWN:
                return game_data.down_arrow
