import asyncio
from random import choice

from color import Color
from game_data import GameData
import pygame as pg
from grid import ColorGrid
from scenes import Scene


async def game() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    PLAY_GRID_DIST_FROM_EDGE: int = (WIND_X) //15

    input_grid: ColorGrid = ColorGrid(
        8,
        8,
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            PLAY_GRID_DIST_FROM_EDGE,
            WIND_Y//2,
            WIND_Y//2,
        )
    )

    solution_grid: ColorGrid = ColorGrid(
        8,
        8,
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            PLAY_GRID_DIST_FROM_EDGE,
            WIND_Y//2,
            WIND_Y//2,
        )
    )

    solution_grid.bounding_rect.right = WIND_X - PLAY_GRID_DIST_FROM_EDGE

    # input_grid.bounding_rect.centery = WIND_Y//2

    for (x, y), _ in solution_grid.get_items():
        solution_grid[(x, y)] = choice(
            [
                Color.BLACK,
                Color.RED,
                Color.GREEN,
            ]
        )
    
    while True:
        dt = clock.tick(max_fps)
        screen.fill(bg_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT

        input_grid.draw(screen)
        solution_grid.draw(screen)

        await asyncio.sleep(0)
        pg.display.update()