from typing import Any, Generator

from color import Color, enum_to_color
import pygame as pg


class ColorGrid:
    def __init__(
            self,
            w: int,
            h: int,
            bounding_rect: pg.Rect,
            default_color: Color = Color.BLACK,
            draw_grid_line: bool=False,
            grid_color: pg.Color=pg.Color("White"),
        ) -> None:
        self.w = w
        self.h = h

        self.cell_w: int = bounding_rect.w // w
        self.cell_h: int = bounding_rect.h // h

        self.bounding_rect = bounding_rect

        self.default_color: Color = default_color

        self.grid: list[list[Color]] = [[default_color for _ in range(w)] for __ in range(h)]

        self.draw_grid_line = draw_grid_line

        self.grid_color = grid_color

    def __getitem__(self, key: tuple[int, int]) -> Color:
        return self.grid[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value: Color):
        self.grid[key[1]][key[0]] = value

    def __contains__(self, item: tuple[int, int]):
        return (item[0] < self.w) and (item[1] < self.h)

    def get_items(self) -> Generator[tuple[tuple[int, int], Color], Any, Any]:
        for y in range(self.h):
            for x in range(self.w):
                yield (x, y), self[x, y]

    def get_rect(self, pos: tuple[int, int]) -> pg.Rect:
        x, y = pos
        topleft = x*self.cell_w + self.bounding_rect.x, y*self.cell_h + self.bounding_rect.y
        rect: pg.Rect = pg.Rect(topleft, (self.cell_w, self.cell_h))
        return rect

    def draw(self, screen: pg.surface.Surface) -> None:
        # pg.draw.rect(
        #     screen,
        #     pg.Color("White"),
        #     self.bounding_rect,
        #     1,
        #     5
        # )

        for (x, y), color in self.get_items():
            rect: pg.Rect = self.get_rect((x, y))
            pg_color = enum_to_color[color]
            pg.draw.rect(
                screen,
                pg_color,
                rect
            )

            if not self.draw_grid_line:
                continue

            pg.draw.rect(
                screen,
                self.grid_color,
                rect,
                5
            )
