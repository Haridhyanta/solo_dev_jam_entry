import asyncio

from game_data import GameData
import pygame as pg
from scenes import Scene


async def level() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    bg_img: pg.surface.Surface = game_data.background_img

    levels_bg_rect = pg.Rect(0, 0, (WIND_X*4)//5, (WIND_Y*4)//5)
    levels_bg_rect.center = WIND_X//2, WIND_Y//2

    LEVEL_BG_RECT_COLOR: pg.Color = pg.Color("White")

    DIST_BTW_LEVEL_RECT_AND_BG: int = WIND_Y // 25
    DIST_BTW_LEVELS: int = WIND_Y // 30

    NO_OF_LEVELS_PER_LINE: int = 6

    LEVEL_W: int = (levels_bg_rect.w - (2*DIST_BTW_LEVEL_RECT_AND_BG + (NO_OF_LEVELS_PER_LINE-1)*DIST_BTW_LEVELS))//NO_OF_LEVELS_PER_LINE
    LEVEL_H: int = LEVEL_W

    LEVEL_DONE_COLOR: pg.Color = pg.Color("Green")
    LEVEL_BORDER_COLOR: pg.Color = pg.Color((216, 90, 26))

    LEVEL_BORDER_W: int = 10
    LEVEL_BORDER_R: int = 5

    LEVEL_NO_FONT: pg.font.Font = game_data.ui_large_font
    LEVEL_NO_COLOR: pg.Color = game_data.text_color

    level_rects: list[pg.Rect] = []
    level_no_sprites: list[pg.surface.Surface] = []

    for i in range(game_data.total_no_of_levels):
        x = levels_bg_rect.x + (i%NO_OF_LEVELS_PER_LINE ) * (LEVEL_W+DIST_BTW_LEVELS) + DIST_BTW_LEVEL_RECT_AND_BG
        y = levels_bg_rect.y + (i//NO_OF_LEVELS_PER_LINE) * (LEVEL_H+DIST_BTW_LEVELS) + DIST_BTW_LEVEL_RECT_AND_BG
        level_rects.append(pg.Rect(x, y, LEVEL_W, LEVEL_H))
        level_no_sprites.append(LEVEL_NO_FONT.render(f'{i+1}', True, LEVEL_NO_COLOR))

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    while True:
        dt = clock.tick(max_fps)
        screen.fill(bg_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue

                for i, level_rect in enumerate(level_rects):
                    if not level_rect.collidepoint(event.pos):
                        continue

                    game_data.level_no = i+1
                    return Scene.GAME
            
        screen.blit(bg_img, (0, 0))

        pg.draw.rect(
            screen,
            LEVEL_BG_RECT_COLOR,
            levels_bg_rect,
            border_radius=2
        )

        for level_rect, level_no_sprite in zip(level_rects, level_no_sprites):
            level_no_rect: pg.Rect = level_no_sprite.get_rect()
            level_no_rect.center = level_rect.center

            pg.draw.rect(
                screen,
                LEVEL_DONE_COLOR,
                level_rect,
                border_radius=2
            )

            pg.draw.rect(
                screen,
                LEVEL_BORDER_COLOR,
                level_rect,
                LEVEL_BORDER_W,
                LEVEL_BORDER_R
            )

            screen.blit(level_no_sprite, level_no_rect)

        pg.display.update()
        await asyncio.sleep(0)