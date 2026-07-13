import asyncio
import enum
from random import choice

from color import Color, enum_to_color
from game_data import GameData
import pygame as pg
from grid import ColorGrid
from load_level import LevelInfo, load_level
from rule import DRSpread, Rule
from scenes import Scene


class Mode(enum.Enum):
    FROZEN = enum.auto()
    NORMAL = enum.auto()
    SPEDUP = enum.auto()
    NOSTEP = enum.auto()

async def game() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    clock: pg.time.Clock = game_data.clock
    max_fps: float = game_data.max_fps
    dt: int = 0

    LEVEL_NO: int = game_data.level_no

    LEVEL_INFO: LevelInfo = load_level(LEVEL_NO)

    DIST_BTW_LEVEL_TEXT_AND_EDGE: int = WIND_Y // 20

    level_text_sprite: pg.surface.Surface = game_data.large_font.render(LEVEL_INFO.name, True, game_data.text_color)
    level_text_rect = level_text_sprite.get_rect()
    level_text_rect.topleft = DIST_BTW_LEVEL_TEXT_AND_EDGE, DIST_BTW_LEVEL_TEXT_AND_EDGE

    DIST_BTW_LEVEL_TEXT_AND_PLAY_GRID = WIND_Y // 25
    PLAY_GRID_DIST_FROM_EDGE: int = (WIND_Y) //20

    input_grid: ColorGrid = ColorGrid(
        len(LEVEL_INFO.solution_grid[0]),
        len(LEVEL_INFO.solution_grid),
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            level_text_rect.bottom + DIST_BTW_LEVEL_TEXT_AND_PLAY_GRID,
            (WIND_Y * 8)//20,
            (WIND_Y * 8)//20,
        ),
        draw_grid_line=True
    )
    
    simulation_grid: ColorGrid = input_grid.copy()

    solution_grid: ColorGrid = ColorGrid(
        len(LEVEL_INFO.solution_grid[0]),
        len(LEVEL_INFO.solution_grid),
        pg.Rect(
            PLAY_GRID_DIST_FROM_EDGE,
            PLAY_GRID_DIST_FROM_EDGE,
            (WIND_Y * 5)//20,
            (WIND_Y * 5)//20,
        ),
        draw_grid_line=True
    )

    solution_grid.grid = LEVEL_INFO.solution_grid

    solution_grid.bounding_rect.bottom = WIND_Y - PLAY_GRID_DIST_FROM_EDGE

    DIST_BTW_RULES_AND_EDGE: int = WIND_Y//17
    DIST_BTW_RULES: int = WIND_Y//30

    current_rule_rect: pg.Rect = pg.Rect(
        0, 
        0,
        WIND_X // 8,
        (WIND_Y * 14) // 30,
    )

    current_rule_rect.bottom = WIND_Y-DIST_BTW_RULES_AND_EDGE
    current_rule_rect.right = WIND_X-DIST_BTW_RULES_AND_EDGE

    RULES_NAME_FONT: pg.font.Font = game_data.bold_font
    RULES_TEXT_FONT: pg.font.Font = game_data.normal_font

    rules_rects: list[pg.Rect] = []
    no_of_rules: int = len(LEVEL_INFO.rules)
    for i in range(no_of_rules):
        rules_rects.append(current_rule_rect.copy())

        current_rule_rect.right = current_rule_rect.left - DIST_BTW_RULES

    rules_rects.reverse()

    rules: list[Rule] = [
        rule_type(
            RULES_NAME_FONT,
            RULES_TEXT_FONT,
            game_data.text_color,
            game_data.text_color,
            game_data.text_outline_color,
            2,
            rules_rects[i],
            pg.Color("White"),
            (rules_rects[i].w * 9 // 10, rules_rects[i].h//11)
        ) for i, rule_type in enumerate(LEVEL_INFO.rules)
    ]

    for rule_i, locked_options in LEVEL_INFO.locked_options.items():
        for option_i, locked_color in locked_options.items():
            rules[rule_i].options[option_i] = locked_color
    
    color_options: list[Color] = LEVEL_INFO.color_options
    color_no_left: list[int] = LEVEL_INFO.color_no_left
    color_option_rects: list[pg.Rect] = []
    selected_color_i: int = -1

    COLOR_OPTION_FONT: pg.font.Font = game_data.large_font
    COLOR_OPTION_OUTLINE_W: int = 5

    COLOR_OPTION_BORDER_DEFAULT_COLOR: pg.Color = pg.Color((250, 95, 28))
    COLOR_OPTION_BORDER_SELECTED_COLOR: pg.Color = pg.Color("White")
    COLOR_OPTION_BORDER_W: int = 5
    COLOR_OPTION_BORDER_R: int = 2

    COLOR_OPTION_SIZE: tuple[int, int] = WIND_Y//10, WIND_Y//10
    DIST_BTW_COLOR_OPTION_AND_EDGE: int = DIST_BTW_RULES_AND_EDGE
    DIST_BTW_COLOR_OPTIONS: int = DIST_BTW_RULES
    DIST_BTW_COLOR_OPTION_AND_RULES: int = WIND_Y//15

    current_option_rect: pg.Rect = pg.Rect((0, 0), COLOR_OPTION_SIZE)
    current_option_rect.right = WIND_X - DIST_BTW_COLOR_OPTION_AND_EDGE
    current_option_rect.bottom = current_rule_rect.top - DIST_BTW_COLOR_OPTION_AND_RULES
    for _ in color_options:
        color_option_rects.append(current_option_rect.copy())
        current_option_rect.right = current_option_rect.left - DIST_BTW_COLOR_OPTIONS

    pause_img: pg.surface.Surface = game_data.pause_img
    unpause_img: pg.surface.Surface = game_data.unpause_img
    step_img: pg.surface.Surface = game_data.step_img

    DIST_BTW_PAUSE_IMG_AND_EDGE: int = WIND_Y // 25
    DIST_BTW_ICONS: int = WIND_Y//30
    pause_rect: pg.Rect = pause_img.get_rect()
    pause_rect.right = WIND_X - DIST_BTW_PAUSE_IMG_AND_EDGE
    pause_rect.top = DIST_BTW_PAUSE_IMG_AND_EDGE

    step_rect: pg.Rect = step_img.get_rect()
    step_rect.center = pause_rect.center
    step_rect.right = pause_rect.left - DIST_BTW_ICONS
    
    winning_screen_bg_rect = pg.Rect(0, 0, (WIND_X*3)//5, (WIND_Y*3)//5)
    winning_screen_bg_rect.center = WIND_X//2, WIND_Y//2

    WINNING_TEXT_COLOR: pg.Color = game_data.text_color
    WINNING_BG_RECT_COLOR: pg.Color = pg.Color("White")
    WINNING_BG_RECT_R: int = 5
    DIST_BTW_WINNING_TEXT_FROM_EDGE: int = WIND_Y//25

    winning_text_sprite: pg.surface.Surface = game_data.ui_large_font.render('YOU WON!', True, WINNING_TEXT_COLOR)
    winning_text_rect: pg.Rect = winning_text_sprite.get_rect()
    winning_text_rect.centerx = winning_screen_bg_rect.centerx
    winning_text_rect.top = winning_screen_bg_rect.top + DIST_BTW_WINNING_TEXT_FROM_EDGE

    DIST_BTW_NEXT_LEVEL_ARROW_AND_EDGE: int = WIND_Y//25

    next_level_img: pg.surface.Surface = game_data.next_level_img
    next_level_rect: pg.Rect = next_level_img.get_rect()
    next_level_rect.right = winning_screen_bg_rect.right - DIST_BTW_NEXT_LEVEL_ARROW_AND_EDGE
    next_level_rect.bottom = winning_screen_bg_rect.bottom - DIST_BTW_NEXT_LEVEL_ARROW_AND_EDGE

    has_won: bool = False

    TIME_BTW_STEPS_MS: int = 100
    TIME_BTW_STEPS_MS_FAST_MODE: int = 10
    
    time_since_last_step_ms = 0
    step_from_i: int = 0

    current_mode: Mode = Mode.NOSTEP

    while True:
        dt = clock.tick(max_fps)
        time_since_last_step_ms+= dt
        screen.fill(bg_color)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return Scene.QUIT
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    game_data.level_no += 1
                    return Scene.GAME
                
                if has_won:
                    continue

                if event.key == pg.K_r:
                    time_since_last_step_ms = 0
                    current_mode = Mode.NOSTEP

                if event.key == pg.K_n:
                    if current_mode != Mode.FROZEN:
                        continue
                    time_since_last_step_ms = 0
                    rules[step_from_i].step(simulation_grid)
                    step_from_i += 1
                    if step_from_i >= len(rules):
                        step_from_i = 0
                    has_won = has_won or simulation_grid.grid == solution_grid.grid

                if event.key == pg.K_k:
                    time_since_last_step_ms = 0
                    if current_mode == Mode.NOSTEP:
                        should_change: bool = True
                        simulation_grid = input_grid.copy()
                        for rule in rules:
                            for option in rule.options:
                                if option is None:
                                    should_change = False
                                    break
                            
                            if not should_change:
                                break

                        if not should_change:
                            continue

                        current_mode = Mode.NORMAL
                        continue

                    if current_mode == Mode.FROZEN:
                        current_mode = Mode.NORMAL
                        continue

                    current_mode = Mode.FROZEN
                    continue
                
                if event.key == pg.K_l:
                    if current_mode == Mode.NORMAL:
                        current_mode = Mode.SPEDUP
                    elif current_mode == Mode.SPEDUP:
                        current_mode = Mode.NORMAL
                continue

            if event.type == pg.MOUSEBUTTONDOWN:
                if has_won:
                    if not next_level_rect.collidepoint(event.pos):
                        continue

                    game_data.level_no += 1
                    return Scene.GAME

                if pause_rect.collidepoint(event.pos):
                    time_since_last_step_ms = 0
                    if current_mode == Mode.NOSTEP:
                        should_change: bool = True
                        simulation_grid = input_grid.copy()
                        for rule in rules:
                            for option in rule.options:
                                if option is None:
                                    should_change = False
                                    break
                            
                            if not should_change:
                                break

                        if not should_change:
                            continue

                        current_mode = Mode.NORMAL
                        continue

                    if current_mode == Mode.FROZEN:
                        current_mode = Mode.NORMAL
                        continue

                    current_mode = Mode.FROZEN
                    continue

                if current_mode != Mode.NOSTEP:
                    if current_mode != Mode.FROZEN:
                        continue
                    if step_rect.collidepoint(event.pos):
                        time_since_last_step_ms = 0
                        rules[step_from_i].step(simulation_grid)
                        step_from_i += 1
                        if step_from_i >= len(rules):
                            step_from_i = 0
                        has_won = has_won or simulation_grid.grid == solution_grid.grid

                    continue

                if event.button != 1:
                    continue

                mouse_pos: tuple[int, int] = event.pos
                matched: bool = False

                for i, option_rect in enumerate(color_option_rects):
                    if not option_rect.collidepoint(mouse_pos):
                        continue

                    matched = True
                    if i==selected_color_i:
                        selected_color_i = -1
                        continue

                    selected_color_i = i
                    break

                if matched:
                    continue

                if selected_color_i < 0:
                    continue

                for rule_i, rule in enumerate(rules):
                    for i, color_input_rect in enumerate(rule.option_rects):
                        if not color_input_rect.collidepoint(mouse_pos):
                            continue

                        matched = True

                        if rule_i in LEVEL_INFO.locked_options:
                            if i in LEVEL_INFO.locked_options[rule_i]:
                                break

                        rule.options[i] = color_options[selected_color_i]
                        break

                    if matched:
                        break

                if matched:
                    continue

                for (x, y), color_value in input_grid.get_items():
                    rect: pg.Rect = input_grid.get_rect((x, y))
                    if not rect.collidepoint(mouse_pos):
                        continue

                    matched = True

                    new_color_value: Color = color_options[selected_color_i]
                    if color_value == new_color_value:
                        input_grid[x, y] = input_grid.default_color
                        color_no_left[selected_color_i] += 1
                        break
                        
                    if color_no_left[selected_color_i] <= 0:
                        break

                    for i, color_option in enumerate(color_options):
                        if color_value == color_option:
                            color_no_left[i] += 1
                            break

                    color_no_left[selected_color_i] -= 1
                    input_grid[x, y] = color_options[selected_color_i]

        if current_mode == Mode.NOSTEP:
            input_grid.draw(screen)
            screen.blit(unpause_img, pause_rect)
        else:
            simulation_grid.draw(screen)
            if current_mode == Mode.FROZEN:
                screen.blit(unpause_img, pause_rect)
            else:
                screen.blit(pause_img, pause_rect)
        solution_grid.draw(screen)

        should_step: bool = False
        if current_mode == Mode.NORMAL:
            should_step = time_since_last_step_ms >= TIME_BTW_STEPS_MS
        elif current_mode == Mode.SPEDUP:
            should_step = time_since_last_step_ms >= TIME_BTW_STEPS_MS_FAST_MODE
        
        if should_step:
            time_since_last_step_ms = 0

        for i, rule in enumerate(rules):
            rule.draw(screen)
            if should_step and i==step_from_i:
                rule.step(simulation_grid)

            if i in LEVEL_INFO.locked_options:
                for locked_option_i in LEVEL_INFO.locked_options[i]:
                    padlock_rect: pg.Rect = game_data.padlock_img.get_rect()

                    padlock_rect.center = rule.option_rects[locked_option_i].center

                    screen.blit(game_data.padlock_img, padlock_rect)

            if current_mode != Mode.NOSTEP and i != step_from_i:
                pixel: pg.Surface = pg.Surface(rule.bg_rect.size, flags=pg.SRCALPHA)
                pixel.fill(game_data.grey_out_color)
                screen.blit(pixel, rule.bg_rect, special_flags=pg.BLEND_RGB_MULT)

        if should_step and not has_won:
            step_from_i += 1
            if step_from_i >= len(rules):
                step_from_i = 0
            has_won = simulation_grid.grid == solution_grid.grid

        for i, (color_value, no_left, option_rect) in enumerate(zip(color_options, color_no_left, color_option_rects)):
            color: pg.Color = enum_to_color[color_value]
            pg.draw.rect(
                screen,
                color,
                option_rect,
                border_radius=COLOR_OPTION_BORDER_R,
            )
            border_color: pg.Color = COLOR_OPTION_BORDER_DEFAULT_COLOR
            if i == selected_color_i:
                border_color = COLOR_OPTION_BORDER_SELECTED_COLOR

            pg.draw.rect(
                screen,
                border_color,
                option_rect,
                width=COLOR_OPTION_BORDER_W,
                border_radius=COLOR_OPTION_BORDER_R,
            )
            
            outline_sprite: pg.surface.Surface = COLOR_OPTION_FONT.render(f'{no_left}', True, game_data.text_outline_color)
            directions: list[tuple[int, int]] = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    directions.append((x*COLOR_OPTION_OUTLINE_W, y*COLOR_OPTION_OUTLINE_W))

            outline_rect: pg.Rect = outline_sprite.get_rect()
            outline_rect.center = option_rect.center

            for (x_offset, y_offset) in directions:
                screen.blit(outline_sprite, outline_rect.move(x_offset, y_offset))

            sprite: pg.surface.Surface = COLOR_OPTION_FONT.render(f'{no_left}', True, game_data.text_color)
            sprite_rect: pg.Rect = sprite.get_rect()
            sprite_rect.center = option_rect.center

            screen.blit(outline_sprite, outline_rect)
            screen.blit(sprite, sprite_rect)

            if current_mode != Mode.NOSTEP:
                pixel: pg.Surface = pg.Surface(option_rect.size, flags=pg.SRCALPHA)
                pixel.fill(game_data.grey_out_color)
                screen.blit(pixel, option_rect, special_flags=pg.BLEND_RGB_MULT)

        outline_sprite: pg.surface.Surface = COLOR_OPTION_FONT.render(LEVEL_INFO.name, True, game_data.text_outline_color)
        directions: list[tuple[int, int]] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                directions.append((x*COLOR_OPTION_OUTLINE_W, y*COLOR_OPTION_OUTLINE_W))

        outline_rect: pg.Rect = outline_sprite.get_rect()
        outline_rect.center = level_text_rect.center

        for (x_offset, y_offset) in directions:
            screen.blit(outline_sprite, outline_rect.move(x_offset, y_offset))

        screen.blit(outline_sprite, outline_rect)
        screen.blit(level_text_sprite, level_text_rect)

        # step option
        screen.blit(step_img, step_rect)
        if current_mode != Mode.FROZEN:
            pixel: pg.Surface = pg.Surface(step_rect.size, flags=pg.SRCALPHA)
            pixel.fill(game_data.grey_out_color)
            screen.blit(pixel, step_rect, special_flags=pg.BLEND_RGB_MULT)

        await asyncio.sleep(0)
        if has_won:
            pg.draw.rect(screen, WINNING_BG_RECT_COLOR, winning_screen_bg_rect, border_radius=WINNING_BG_RECT_R)
            screen.blit(winning_text_sprite, winning_text_rect)

            screen.blit(next_level_img, next_level_rect)
        pg.display.update()