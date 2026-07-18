import asyncio
import enum
from random import choice

from color import Color, enum_to_color
from game_data import GameData
import pygame as pg
from grid import ColorGrid
from load_level import LevelInfo, load_level
from rule import SESpread, Rule
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

    DIST_BTW_HOME_IMG_AND_EDGE: int = 0# WIND_Y // 25

    normal_home_img: pg.surface.Surface = game_data.home_img
    normal_home_rect: pg.Rect = normal_home_img.get_rect()
    normal_home_rect.topleft = DIST_BTW_HOME_IMG_AND_EDGE, DIST_BTW_HOME_IMG_AND_EDGE

    audio_on_img: pg.surface.Surface = game_data.audio_on_img
    audio_off_img: pg.surface.Surface = game_data.audio_off_img
    audio_rect: pg.Rect = audio_on_img.get_rect()
    audio_rect.topleft = normal_home_rect.topright

    LEVEL_NO: int = game_data.level_no

    LEVEL_INFO: LevelInfo = load_level(LEVEL_NO)

    DIST_BTW_LEVEL_TEXT_AND_EDGE: int = WIND_Y // 20
    DIST_BTW_HOME_IMG_AND_LEVEL_TEXT: int = WIND_Y // 25

    level_text_sprite: pg.surface.Surface = game_data.large_font.render(LEVEL_INFO.name, True, game_data.text_color)
    level_text_rect = level_text_sprite.get_rect()
    level_text_rect.left = audio_rect.right + DIST_BTW_HOME_IMG_AND_LEVEL_TEXT
    level_text_rect.top = DIST_BTW_LEVEL_TEXT_AND_EDGE

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

    TARGET_FONT: pg.font.Font = game_data.large_font
    TARGET_TEXT_SPRITE: pg.surface.Surface = TARGET_FONT.render('TARGET:', True, game_data.text_color)
    target_text_rect = TARGET_TEXT_SPRITE.get_rect()
    target_text_rect.bottomleft = solution_grid.bounding_rect.topleft

    DIST_BTW_RULES_AND_EDGE: int = WIND_Y//17
    DIST_BTW_RULES: int = WIND_Y//30

    current_rule_rect: pg.Rect = pg.Rect(
        0, 
        0,
        (WIND_X * 13) // 100,
        (WIND_Y * 17) // 30,
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
    COLOR_OPTION_BORDER_W: int = 25
    COLOR_OPTION_BORDER_R: int = 10

    COLOR_OPTION_SIZE: tuple[int, int] = WIND_Y//7, WIND_Y//7
    DIST_BTW_COLOR_OPTION_AND_EDGE: int = DIST_BTW_RULES_AND_EDGE
    DIST_BTW_COLOR_OPTIONS: int = DIST_BTW_RULES
    DIST_BTW_COLOR_OPTION_AND_RULES: int = WIND_Y//35

    current_option_rect: pg.Rect = pg.Rect((0, 0), COLOR_OPTION_SIZE)
    current_option_rect.right = WIND_X - DIST_BTW_COLOR_OPTION_AND_EDGE
    current_option_rect.bottom = current_rule_rect.top - DIST_BTW_COLOR_OPTION_AND_RULES
    for _ in color_options:
        color_option_rects.append(current_option_rect.copy())
        current_option_rect.right = current_option_rect.left - DIST_BTW_COLOR_OPTIONS

    can_unpause: bool = False

    pause_img: pg.surface.Surface = game_data.pause_img
    unpause_img: pg.surface.Surface = game_data.unpause_img
    step_img: pg.surface.Surface = game_data.step_img
    reset_img: pg.surface.Surface = game_data.reset_img

    DIST_BTW_PAUSE_IMG_AND_EDGE: int = WIND_Y // 25
    DIST_BTW_ICONS: int = WIND_Y//30
    pause_rect: pg.Rect = pause_img.get_rect()
    pause_rect.right = WIND_X - DIST_BTW_PAUSE_IMG_AND_EDGE
    pause_rect.top = DIST_BTW_PAUSE_IMG_AND_EDGE

    step_rect: pg.Rect = step_img.get_rect()
    step_rect.center = pause_rect.center
    step_rect.right = pause_rect.left - DIST_BTW_ICONS
    
    reset_rect: pg.Rect = reset_img.get_rect()
    reset_rect.center= step_rect.center
    reset_rect.right = step_rect.left - DIST_BTW_ICONS
    
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

    DIST_BTW_WINNING_ICONS_AND_EDGE: int = WIND_Y//25

    next_level_img: pg.surface.Surface = game_data.next_level_img
    next_level_rect: pg.Rect = next_level_img.get_rect()
    next_level_rect.right = winning_screen_bg_rect.right - DIST_BTW_WINNING_ICONS_AND_EDGE
    next_level_rect.bottom = winning_screen_bg_rect.bottom - DIST_BTW_WINNING_ICONS_AND_EDGE

    winning_home_img: pg.surface.Surface = game_data.home_img
    winning_home_rect: pg.Rect = winning_home_img.get_rect()
    winning_home_rect.left = winning_screen_bg_rect.left + DIST_BTW_WINNING_ICONS_AND_EDGE
    winning_home_rect.bottom = winning_screen_bg_rect.bottom - DIST_BTW_WINNING_ICONS_AND_EDGE

    has_won: bool = False

    TIME_BTW_STEPS_MS: int = 200
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
                if audio_rect.collidepoint(event.pos):
                    game_data.music_is_paused = not game_data.music_is_paused
                    if game_data.music_is_paused:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                    continue
                if has_won:
                    game_data.max_level_no = max(LEVEL_NO+1, game_data.max_level_no)
                    if next_level_rect.collidepoint(event.pos):
                        game_data.level_no += 1
                        if game_data.level_no > game_data.total_no_of_levels:
                            return Scene.THANKS
                        return Scene.GAME

                    if winning_home_rect.collidepoint(event.pos):
                        return Scene.HOME

                    continue

                if normal_home_rect.collidepoint(event.pos):
                    return Scene.HOME

                if pause_rect.collidepoint(event.pos):
                    time_since_last_step_ms = 0
                    if current_mode == Mode.NOSTEP:
                        if not can_unpause:
                            continue
                        selected_color_i = -1
                        current_mode = Mode.NORMAL
                        simulation_grid= input_grid.copy()
                        continue
                    if current_mode == Mode.FROZEN:
                        selected_color_i = -1
                        current_mode = Mode.NORMAL
                        continue

                    current_mode = Mode.FROZEN
                    continue

                if current_mode != Mode.NOSTEP:
                    if reset_rect.collidepoint(event.pos):
                        time_since_last_step_ms = 0
                        step_from_i = 0
                        current_mode = Mode.NOSTEP

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
            can_unpause = True
            for rule in rules:
                for option in rule.options:
                    if option is None:
                        can_unpause = False
                        break
                
                if not can_unpause:
                    break

        if current_mode == Mode.NOSTEP:
            input_grid.draw(screen)
            screen.blit(unpause_img, pause_rect)
            if not can_unpause:
                pixel: pg.Surface = pg.Surface(pause_rect.size, flags=pg.SRCALPHA)
                pixel.fill(game_data.grey_out_color)
                screen.blit(pixel, pause_rect, special_flags=pg.BLEND_RGB_MULT)
        else:
            simulation_grid.draw(screen)
            if current_mode == Mode.FROZEN:
                screen.blit(unpause_img, pause_rect)
            else:
                screen.blit(pause_img, pause_rect)
        solution_grid.draw(screen)

        outline_sprite: pg.surface.Surface = COLOR_OPTION_FONT.render('TARGET:', True, game_data.text_outline_color)
        directions: list[tuple[int, int]] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                directions.append((x*COLOR_OPTION_OUTLINE_W, y*COLOR_OPTION_OUTLINE_W))

        for (x_offset, y_offset) in directions:
            screen.blit(outline_sprite, target_text_rect.move(x_offset, y_offset))
        screen.blit(outline_sprite, target_text_rect)
        screen.blit(TARGET_TEXT_SPRITE, target_text_rect)

        should_step: bool = False
        if current_mode == Mode.NORMAL:
            should_step = time_since_last_step_ms >= TIME_BTW_STEPS_MS
        elif current_mode == Mode.SPEDUP:
            should_step = time_since_last_step_ms >= TIME_BTW_STEPS_MS_FAST_MODE
        
        should_step = should_step and not has_won

        if should_step:
            time_since_last_step_ms = 0

        for i, rule in enumerate(rules):
            rule.draw(
                screen,
                selected_color_i>=0,
                COLOR_OPTION_BORDER_DEFAULT_COLOR,
            )
            if should_step and i==step_from_i:
                rule.step(simulation_grid)

            if current_mode != Mode.NOSTEP and i==step_from_i:
                try: 
                    rule.draw_arrow(screen, simulation_grid)
                except NotImplementedError:
                    pass

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

        # normal home icon
        pg.draw.rect(
            screen,
            pg.Color("White"),
                normal_home_rect.inflate(20, 20),
            10
        )
        screen.blit(normal_home_img, normal_home_rect)

        # audio icon
        pg.draw.rect(
            screen,
            pg.Color("White"),
                audio_rect.inflate(20, 20),
            10
        )
        screen.blit(audio_off_img if game_data.music_is_paused else audio_on_img, audio_rect)

        # step and reset option
        screen.blit(step_img, step_rect)
        screen.blit(reset_img, reset_rect)
        pixel: pg.Surface = pg.Surface(step_rect.size, flags=pg.SRCALPHA)
        pixel.fill(game_data.grey_out_color)
        if current_mode == Mode.NOSTEP:
            screen.blit(pixel, reset_rect, special_flags=pg.BLEND_RGB_MULT)
        if current_mode != Mode.FROZEN:
            screen.blit(pixel, step_rect, special_flags=pg.BLEND_RGB_MULT)
        
        # Tutorial prompts
        if LEVEL_NO == 1:
            if selected_color_i < 0 and current_mode == Mode.NOSTEP:
                tutorial_prompt_rect: pg.Rect = game_data.tutorial_prompt_1.get_rect()
                tutorial_prompt_rect.midright = color_option_rects[0].midleft
                screen.blit(game_data.tutorial_prompt_1, tutorial_prompt_rect)
            elif not any([any([color != Color.BLACK for color in row]) for row in input_grid.grid]):
                tutorial_prompt_rect: pg.Rect = game_data.tutorial_prompt_2.get_rect()
                tutorial_prompt_rect.midleft = input_grid.get_rect((0, 0)).midright
                screen.blit(game_data.tutorial_prompt_2, tutorial_prompt_rect)
            elif rules[0].options[0] is None:
                tutorial_prompt_rect: pg.Rect = game_data.tutorial_prompt_3.get_rect()
                tutorial_prompt_rect.midright = rules[0].option_rects[0].midleft
                screen.blit(game_data.tutorial_prompt_3, tutorial_prompt_rect)
            elif current_mode == Mode.NOSTEP:
                tutorial_prompt_rect: pg.Rect = game_data.tutorial_prompt_4.get_rect()
                tutorial_prompt_rect.midtop = pause_rect.midbottom
                screen.blit(game_data.tutorial_prompt_4, tutorial_prompt_rect)
            else:
                tutorial_prompt_rect: pg.Rect = game_data.tutorial_prompt_5.get_rect()
                tutorial_prompt_rect.midleft = solution_grid.bounding_rect.midright
                screen.blit(game_data.tutorial_prompt_5, tutorial_prompt_rect)

        if has_won:
            pg.draw.rect(screen, WINNING_BG_RECT_COLOR, winning_screen_bg_rect, border_radius=WINNING_BG_RECT_R)
            screen.blit(winning_text_sprite, winning_text_rect)

            screen.blit(next_level_img, next_level_rect)

            screen.blit(winning_home_img, winning_home_rect)

        pg.display.update()
        await asyncio.sleep(0)