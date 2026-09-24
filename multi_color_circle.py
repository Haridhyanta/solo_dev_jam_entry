from math import pi

import pygame as pg


def get_multi_color_circle(
        diameter: int,
        colors: list[pg.Color],
        bg_color: pg.Color=pg.Color(0, 0, 0, 0)
    ) -> pg.surface.Surface:
    circle_surface: pg.surface.Surface = pg.surface.Surface((diameter, diameter), flags=pg.SRCALPHA)
    circle_surface.fill(bg_color)
    bg_rect: pg.Rect = pg.Rect(0, 0, diameter, diameter)

    angle: float = 2*pi/len(colors)

    for i, color in enumerate(colors):
        pg.draw.arc(
            circle_surface,
            color,
            bg_rect,
            i*angle,
            (i+1)*angle,
            200
        )

    return circle_surface
