import pygame as pg
from pygame.font import Font

from color import Color, enum_to_color
from direction import Direction
from game_data import GameData
from grid import ColorGrid
from helper_func import text_wrap_mono


class Rule:
    def __init__(
            self,
            name: str,
            text: list[str],
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
            dist_btw_option_and_text: int=15
        ) -> None:

        self.name: str = name
        self.text: list[str] = text
        self.name_font: pg.font.Font = name_font
        self.text_font: pg.font.Font = text_font
        self.name_color: pg.Color = name_color
        self.text_color: pg.Color = text_color
        self.outline_color: pg.Color = outline_color
        self.outline_width: int = outline_width
        self.bg_rect: pg.Rect = bg_rect
        self.bg_color: pg.Color = bg_color
        self.option_size: tuple[int, int] = option_size

        self.text_sprites: list[pg.surface.Surface] = []
        self.text_sprite_rects: list[pg.Rect] = []

        self.no_of_options: int = len(text)-1
        self.option_rects: list[pg.Rect] = [pg.Rect((0, 0), option_size) for _ in range(self.no_of_options)]
        self.options: list[Color|None] = [None] * self.no_of_options

        self.name_sprite: pg.surface.Surface = text_wrap_mono(
            name_font,
            name,
            self.bg_rect.w * 8 // 10,
            name_color,
            center_text=True
        )
        self.name_sprite_rect: pg.Rect = self.name_sprite.get_rect()
        self.name_sprite_rect.midtop = bg_rect.midtop

        for para in self.text:
            sprite: pg.surface.Surface = text_wrap_mono(text_font, para, bg_rect.w, text_color)
            self.text_sprites.append(sprite)
            self.text_sprite_rects.append(sprite.get_rect())

        last_rect: pg.Rect = self.name_sprite_rect

        for i in range(0, 2*len(text)-1):
            if i%2 == 1:
                index = (i-1)//2
                self.option_rects[index].top = last_rect.bottom + dist_btw_option_and_text
                self.option_rects[index].centerx = bg_rect.centerx
                last_rect = self.option_rects[index]
            else:
                index = i//2
                self.text_sprite_rects[index].top = last_rect.bottom + dist_btw_option_and_text
                self.text_sprite_rects[index].left = bg_rect.left
                last_rect = self.text_sprite_rects[index]

    def step(self, grid: ColorGrid) -> None:
        raise NotImplementedError()
    
    def draw(
            self, 
            screen: pg.surface.Surface,
            draw_border: bool=False,
            border_color: pg.Color=pg.Color(250, 95, 28),
            border_w: int=15
        ) -> None:
        pg.draw.rect(
            screen,
            self.bg_color,
            self.bg_rect
        )

        pg.draw.rect(
            screen,
            self.text_color,
            pg.Rect(*self.bg_rect.topleft, self.bg_rect.w, self.name_sprite_rect.h),
            7,
        )
        screen.blit(self.name_sprite, self.name_sprite_rect)

        for text_sprite, text_sprite_rect in zip(self.text_sprites, self.text_sprite_rects):
            screen.blit(text_sprite, text_sprite_rect)

        for option_rect, option_color in zip(self.option_rects, self.options):
            if option_color is None:
                if draw_border:
                    pg.draw.rect(
                        screen,
                        border_color,
                        option_rect.inflate(2*border_w, 2*border_w),
                    )

                pg.draw.rect(
                    screen,
                    pg.Color("Black"),
                    option_rect
                )
                outline_sprite: pg.surface.Surface = self.text_font.render("NOT SELECTED", True, self.outline_color)
                outline_width = self.outline_width
                directions: list[tuple[int, int]] = []
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        directions.append((x*outline_width, y*outline_width))

                outline_rect: pg.Rect = outline_sprite.get_rect()
                outline_rect.center = option_rect.center

                for (x_offset, y_offset) in directions:
                    screen.blit(outline_sprite, outline_rect.move(x_offset, y_offset))

                sprite: pg.surface.Surface = self.text_font.render("NOT SELECTED", True, pg.Color("White"))
                sprite_rect: pg.Rect = sprite.get_rect()
                sprite_rect.center = option_rect.center

                # screen.blit(outline_sprite, outline_rect)
                screen.blit(sprite, sprite_rect)
                continue
                
            pg.draw.rect(
                screen,
                enum_to_color[option_color],
                option_rect
            )

    def draw_arrow(self, surface: pg.surface.Surface, grid: ColorGrid) -> None:
        raise NotImplementedError()

class Spread(Rule):
    def __init__(
        self,
        name_font: Font,
        text_font: Font,
        name_color: pg.Color,
        text_color: pg.Color,
        outline_color: pg.Color,
        outline_width: int,
        bg_rect: pg.Rect,
        bg_color: pg.Color,
        option_size: tuple[int, int],
        dist_btw_option_and_text: int = 15,
        name: str|None=None,
        text: list[str]|None=None,
        directions: list[Direction]|None=None,
    ) -> None:
        name = 'Spread' if name is None else name
        text = ['The color', 'spreads to every square adjacent to it.'] if text is None else text
        super().__init__(
            name,
            text,
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            dist_btw_option_and_text
        )

        self.directions: list[Direction] = [
            Direction.RIGHT,
            Direction.LEFT,
            Direction.UP,
            Direction.DOWN
        ] if directions is None else directions

        self.option_rects[0] = pg.Rect((0, 0), option_size)
        bounding_rect: pg.Rect = self.option_rects[0].copy()

        self.arrow_rects: list[pg.Rect] = []
        arrow_img_rect: pg.Rect = GameData().up_arrow.get_rect()

        for direction in self.directions:
            arrow_rect = arrow_img_rect.copy()
            direction.align_edge_to_edge(arrow_rect, self.option_rects[0])
            self.arrow_rects.append(arrow_rect)

        bounding_rect = bounding_rect.unionall(self.arrow_rects)
        old_bounding_rect: pg.Rect = bounding_rect.copy()

        body_w, body_h = bg_rect.w, bg_rect.h-self.name_sprite_rect.h
        body_rect: pg.Rect = pg.Rect(0, 0, body_w, body_h)
        body_rect.scale_by_ip(0.95, 0.95)
        body_rect.centerx = self.bg_rect.centerx
        body_rect.top = self.name_sprite_rect.bottom

        bounding_rect = body_rect.fit(bounding_rect)

        bounding_rect.center = body_rect.center

        self.scale: float = 0.8 # bounding_rect.w/old_bounding_rect.w

        x_offset: int = self.option_rects[0].x-old_bounding_rect.x
        y_offset: int = self.option_rects[0].y-old_bounding_rect.y
        self.option_rects[0].x = round(bounding_rect.x + x_offset * self.scale)
        self.option_rects[0].y = round(bounding_rect.y + y_offset * self.scale)
        self.option_rects[0].w = round(self.option_rects[0].w * self.scale)
        self.option_rects[0].h = round(self.option_rects[0].h * self.scale)

        for arrow_rect in self.arrow_rects:
            x_offset: int = arrow_rect.x-old_bounding_rect.x
            y_offset: int = arrow_rect.y-old_bounding_rect.y
            arrow_rect.x = round(bounding_rect.x + x_offset * self.scale)
            arrow_rect.y = round(bounding_rect.y + y_offset * self.scale)
            arrow_rect.w = round(arrow_rect.w * self.scale)
            arrow_rect.h = round(arrow_rect.h * self.scale)

    def step(self, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return
        new_squares: list[tuple[int, int]] = []
        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                new_squares.append(next_sq)

        for pos in new_squares:
            grid[pos] = selected_color

    def draw_arrow(self, surface: pg.Surface, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return

        game_data: GameData = GameData()

        arrow_rect: pg.Rect = game_data.up_arrow.get_rect()

        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            current_rect: pg.Rect = grid.get_rect((x, y))

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                if grid[next_sq] == selected_color:
                    continue

                dir.align_center_to_edge(arrow_rect, current_rect)
                surface.blit(dir.get_arrow(game_data), arrow_rect)

    def draw(
        self,
        screen: pg.Surface,
        draw_border: bool = False,
        border_color: pg.Color = pg.Color(250, 95, 28),
        border_w: int = 15
    ) -> None:
        pg.draw.rect(
            screen,
            self.bg_color,
            self.bg_rect
        )

        pg.draw.rect(
            screen,
            self.text_color,
            pg.Rect(*self.bg_rect.topleft, self.bg_rect.w, self.name_sprite_rect.h),
            7,
        )
        screen.blit(self.name_sprite, self.name_sprite_rect)

        if self.options[0] is None:
            if draw_border:
                pg.draw.rect(
                    screen,
                    border_color,
                    self.option_rects[0].inflate(2*border_w, 2*border_w),
                )

            pg.draw.rect(
                screen,
                pg.Color("Black"),
                self.option_rects[0]
            )

            sprite: pg.surface.Surface = self.text_font.render("?", True, pg.Color("White"))
            sprite_rect: pg.Rect = sprite.get_rect()
            sprite_rect.center = self.option_rects[0].center

            # screen.blit(outline_sprite, outline_rect)
            screen.blit(sprite, sprite_rect)
        else: 
            pg.draw.rect(
                screen,
                enum_to_color[self.options[0]],
                self.option_rects[0]
            )

        for direction, arrow_rect in zip(self.directions, self.arrow_rects):
            screen.blit(pg.transform.scale_by(direction.get_arrow(GameData()), self.scale), arrow_rect)

class NESpread(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Right Spread"
        text: list[str] = ["The color", "spreads to the squares above and to the right of it."]
        directions = [
            Direction.UP,
            Direction.RIGHT
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class SESpread(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Right Spread"
        text: list[str] = ["The color", "spreads to the squares below and to the right of it."]
        directions = [
            Direction.DOWN,
            Direction.RIGHT
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class SWSpread(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Left Spread"
        text: list[str] = ["The color", "spreads to the squares below and to the left of it."]
        directions = [
            Direction.DOWN,
            Direction.LEFT
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class NWSpread(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Left Spread"
        text: list[str] = ["The color", "spreads to the squares above and to the left of it."]
        directions = [
            Direction.UP,
            Direction.LEFT
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class Cover(Rule):
    def __init__(
        self,
        name_font: Font,
        text_font: Font,
        name_color: pg.Color,
        text_color: pg.Color,
        outline_color: pg.Color,
        outline_width: int,
        bg_rect: pg.Rect,
        bg_color: pg.Color,
        option_size: tuple[int, int],
        dist_btw_option_and_text: int = 15,
        name: str|None=None,
        text: list[str]|None=None
    ) -> None:
        name = 'Cover' if name is None else name
        text = ['The color', 'spreads to every square adjacent to it unless the square is of color', ''] if text is None else text
        super().__init__(
            name,
            text,
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            dist_btw_option_and_text
        )

        self.directions: list[Direction] = [
            Direction.RIGHT,
            Direction.LEFT,
            Direction.UP,
            Direction.DOWN
        ]

    def step(self, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return

        cover_color = self.options[1]
        if cover_color is None:
            return

        new_squares: list[tuple[int, int]] = []
        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                if grid[next_sq] == cover_color:
                    continue

                new_squares.append(next_sq)

        for pos in new_squares:
            grid[pos] = selected_color

    def draw_arrow(self, surface: pg.Surface, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return

        cover_color = self.options[1]
        if cover_color is None:
            return

        game_data: GameData = GameData()

        arrow_rect: pg.Rect = game_data.up_arrow.get_rect()

        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            current_rect: pg.Rect = grid.get_rect((x, y))

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                if grid[next_sq] == selected_color:
                    continue

                dir.align_center_to_edge(arrow_rect, current_rect)
                surface.blit(dir.get_arrow(game_data), arrow_rect)

                if grid[next_sq] == cover_color:
                    surface.blit(game_data.x_img, arrow_rect)

class NECover(Cover):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Right Cover"
        text: list[str] = ["The color", "spreads to the squares above and to the right of it unless it is of the color", ""]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.UP,
            Direction.RIGHT
        ]

class SECover(Cover):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Right Cover"
        text: list[str] = ["The color", "spreads to the squares below and to the right of it unless it is of the color", ""]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.DOWN,
            Direction.RIGHT
        ]

class SWCover(Cover):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Left Cover"
        text: list[str] = ["The color", "spreads to the squares below and to the left of it unless it is of the color", ""]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.DOWN,
            Direction.LEFT
        ]

class NWCover(Cover):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Left Cover"
        text: list[str] = ["The color", "spreads to the squares above and to the left of it unless it is of the color", ""]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.UP,
            Direction.LEFT
        ]

class Replace(Rule):
    def __init__(
        self,
        name_font: Font,
        text_font: Font,
        name_color: pg.Color,
        text_color: pg.Color,
        outline_color: pg.Color,
        outline_width: int,
        bg_rect: pg.Rect,
        bg_color: pg.Color,
        option_size: tuple[int, int],
        dist_btw_option_and_text: int = 15,
        name: str|None=None,
        text: list[str]|None=None
    ) -> None:
        name = 'Replace' if name is None else name
        text = ['The color', 'spreads to every square adjacent to it only if the squares of color', ''] if text is None else text
        super().__init__(
            name,
            text,
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            dist_btw_option_and_text
        )

        self.directions: list[Direction] = [
            Direction.RIGHT,
            Direction.LEFT,
            Direction.UP,
            Direction.DOWN
        ]

    def step(self, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return
        
        replace_color = self.options[1]
        if replace_color is None:
            return

        new_squares: list[tuple[int, int]] = []
        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                if grid[next_sq] != replace_color:
                    continue

                new_squares.append(next_sq)

        for pos in new_squares:
            grid[pos] = selected_color

    def draw_arrow(self, surface: pg.Surface, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return
        
        replace_color = self.options[1]
        if replace_color is None:
            return

        game_data: GameData = GameData()

        arrow_rect: pg.Rect = game_data.up_arrow.get_rect()
        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            current_rect: pg.Rect = grid.get_rect((x, y))

            for dir in self.directions:
                next_sq = dir.next((x, y))

                if next_sq not in grid:
                    continue

                if grid[next_sq] == selected_color:
                    continue

                dir.align_center_to_edge(arrow_rect, current_rect)
                surface.blit(dir.get_arrow(game_data), arrow_rect)

                if grid[next_sq] != replace_color:
                    surface.blit(game_data.x_img, arrow_rect)

class NEReplace(Replace):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Right Replace"
        text: list[str] = [
            "The color",
            "spreads to the squares above and to the right of it if the squares are of color",
            ""
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.UP,
            Direction.RIGHT
        ]

class SEReplace(Replace):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Right Replace"
        text: list[str] = [
            "The color",
            "spreads to the squares below and to the right of it if the squares are of color",
            ""
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.DOWN,
            Direction.RIGHT
        ]

class SWReplace(Replace):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Left Replace"
        text: list[str] = [
            "The color",
            "spreads to the squares below and to the left of it if the squares are of color",
            ""
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.DOWN,
            Direction.LEFT
        ]

class NWReplace(Replace):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up Left Replace"
        text: list[str] = [
            "The color",
            "spreads to the squares below and to the left of it if the squares are of color",
            ""
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
        )
        self.directions = [
            Direction.UP,
            Direction.LEFT
        ]

class NMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Up March"
        text: list[str] = [
            "The color", 
            "spreads to the squares directly above it."
        ]
        directions = [
            Direction.UP,
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class EMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Right March"
        text: list[str] = [
            "The color", 
            "spreads to the squares directly to the right of it."
        ]
        directions = [
            Direction.RIGHT,
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class SMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down March"
        text: list[str] = [
            "The color", 
            "spreads to the squares directly below it."
        ]
        directions = [
            Direction.DOWN,
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class WMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Left March"
        text: list[str] = [
            "The color", 
            "spreads to the squares directly to the left of it."
        ]
        directions = [
            Direction.LEFT,
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class HMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Horizontal March"
        text: list[str] = [
            "The color", 
            "spreads horizontally"
        ]
        directions = [
            Direction.LEFT,
            Direction.RIGHT
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

class VMarch(Spread):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            outline_color: pg.Color,
            outline_width: int,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Vertical March"
        text: list[str] = [
            "The color", 
            "spreads vertically"
        ]
        directions = [
            Direction.UP,
            Direction.DOWN
        ]
        super().__init__(
            name_font,
            text_font,
            name_color,
            text_color,
            outline_color,
            outline_width,
            bg_rect,
            bg_color,
            option_size,
            name=name,
            text=text,
            directions=directions,
        )

NAME_TO_RULE: dict[str, type] = {
    "Spread": Spread,
    "N-E Spread": NESpread,
    "S-E Spread": SESpread,
    "S-W Spread": SWSpread,
    "N-W Spread": NWSpread,

    "Cover": Cover,
    "N-E Cover": NECover,
    "S-E Cover": SECover,
    "S-W Cover": SWCover,
    "N-W Cover": NWCover,

    "Replace": Replace,
    "N-E Replace": NEReplace,
    "S-E Replace": SEReplace,
    "S-W Replace": SWReplace,
    "N-W Replace": NWReplace,

    "N March": NMarch,
    "E March": EMarch,
    "S March": SMarch,
    "W March": WMarch,
    "H March": HMarch,
    "V March": VMarch,
}
