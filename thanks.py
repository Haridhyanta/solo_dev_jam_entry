import asyncio

from game_data import GameData
import pygame as pg
from helper_func import text_sprite
from scenes import Scene


async def thanks() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    THANK_YOU_SPRITE = text_sprite(
        game_data.ui_max_font,
        'THANK YOU\nFOR PLAYING',
        pg.Color("Green"),
        center_text=True
    )

    thank_you_rect: pg.Rect = THANK_YOU_SPRITE.get_rect()
    thank_you_rect.center = WIND_X//2, WIND_Y//2

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    while True:
        dt = clock.tick(max_fps)
        screen.fill(bg_color)
        screen.blit(game_data.background_img, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT
            
        screen.blit(THANK_YOU_SPRITE, thank_you_rect)
        pg.display.update()
        await asyncio.sleep(0)