import asyncio
from random import choice

from color import Color
from game_data import GameData
import pygame as pg
from grid import ColorGrid
from rule import DRSpread, Rule
from scenes import Scene


async def game() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    PLAY_GRID_DIST_FROM_EDGE: int = (WIND_X) //17

    input_grid: ColorGrid = ColorGrid(
        8,
        8,
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            PLAY_GRID_DIST_FROM_EDGE,
            (WIND_Y * 2)//5,
            (WIND_Y * 2)//5,
        )
    )

    solution_grid: ColorGrid = ColorGrid(
        8,
        8,
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            PLAY_GRID_DIST_FROM_EDGE,
            (WIND_Y * 2)//5,
            (WIND_Y * 2)//5,
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

    DIST_BTW_RULES_AND_EDGE: int = WIND_X//15
    DIST_BTW_RULES: int = WIND_X//20

    current_rule_rect: pg.Rect = pg.Rect(
        0, 
        0,
        WIND_X // 5,
        WIND_Y // 3,
    )

    current_rule_rect.bottomleft = DIST_BTW_RULES_AND_EDGE, WIND_Y-DIST_BTW_RULES_AND_EDGE

    RULES_NAME_FONT: pg.font.Font = game_data.normal_font
    RULES_TEXT_FONT: pg.font.Font = game_data.bold_font

    rules_rects: list[pg.Rect] = []
    no_of_rules: int = 1
    for i in range(no_of_rules):
        rules_rects.append(current_rule_rect.copy())

        current_rule_rect.left = current_rule_rect.right + DIST_BTW_RULES

    rules: list[Rule] = [
        DRSpread(
            RULES_NAME_FONT,
            RULES_TEXT_FONT,
            game_data.text_color,
            game_data.text_color,
            rules_rects[0],
            pg.Color("White"),
            (rules_rects[0].w * 9 // 10, rules_rects[0].h//10)
        ),
    ]
    
    while True:
        dt = clock.tick(max_fps)
        screen.fill(bg_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    for rule in rules:
                        rule.step(input_grid)

        input_grid.draw(screen)
        solution_grid.draw(screen)

        for rule in rules:
            rule.draw(screen)

        await asyncio.sleep(0)
        pg.display.update()