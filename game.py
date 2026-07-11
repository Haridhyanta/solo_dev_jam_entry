import asyncio

from game_data import GameData
import pygame as pg
from scenes import Scene


async def game() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    while True:
        dt = clock.tick(max_fps)
        screen.fill(bg_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT

        await asyncio.sleep(0)
        pg.display.update()