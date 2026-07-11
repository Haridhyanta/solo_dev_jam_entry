import pygame as pg
from pygame.font import Font

from color import Color, enum_to_color
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
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:

        self.name: str = name
        self.text: list[str] = text
        self.name_font: pg.font.Font = name_font
        self.text_font: pg.font.Font = text_font
        self.name_color: pg.Color = name_color
        self.text_color: pg.Color = text_color
        self.bg_rect: pg.Rect = bg_rect
        self.bg_color: pg.Color = bg_color
        self.option_size: tuple[int, int] = option_size

        self.text_sprites: list[pg.surface.Surface] = []
        self.text_sprite_rects: list[pg.Rect] = []

        self.no_of_options: int = len(text)-1
        self.option_rects: list[pg.Rect] = [pg.Rect((0, 0), option_size) for _ in range(self.no_of_options)]
        self.options: list[Color|None] = [None] * self.no_of_options

        self.name_sprite: pg.surface.Surface = name_font.render(name, True, name_color)
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
                self.option_rects[index].top = last_rect.bottom
                self.option_rects[index].centerx = bg_rect.centerx
                last_rect = self.option_rects[index]
            else:
                index = i//2
                self.text_sprite_rects[index].top = last_rect.bottom
                self.text_sprite_rects[index].left = bg_rect.left
                last_rect = self.text_sprite_rects[index]

    def step(self, grid: ColorGrid) -> None:
        raise NotImplementedError()
    
    def draw(self, screen: pg.surface.Surface) -> None:
        pg.draw.rect(
            screen,
            self.bg_color,
            self.bg_rect
        )

        screen.blit(self.name_sprite, self.name_sprite_rect)

        for text_sprite, text_sprite_rect in zip(self.text_sprites, self.text_sprite_rects):
            screen.blit(text_sprite, text_sprite_rect)

        for option_rect, option_color in zip(self.option_rects, self.options):
            if option_color is None:
                pg.draw.rect(
                    screen,
                    pg.Color("Black"),
                    option_rect
                )

                sprite: pg.surface.Surface = self.text_font.render("?", True, self.text_color)
                sprite_rect: pg.Rect = sprite.get_rect()
                sprite_rect.center = option_rect.center

                screen.blit(sprite, sprite_rect)
                continue
                
            pg.draw.rect(
                screen,
                enum_to_color[option_color],
                option_rect
            )

class DRSpread(Rule):
    def __init__(
            self,
            name_font: pg.font.Font,
            text_font: pg.font.Font,
            name_color: pg.Color,
            text_color: pg.Color,
            bg_rect: pg.Rect,
            bg_color: pg.Color,
            option_size: tuple[int, int],
        ) -> None:
        name: str = "Down Right Spread"
        text: list[str] = ["The color", "spreads to the squares bellow and to the right of it."]
        super().__init__(name, text, name_font, text_font, name_color, text_color, bg_rect, bg_color, option_size)

    def step(self, grid: ColorGrid) -> None:
        selected_color = self.options[0]
        if selected_color is None:
            return
        new_squares: list[tuple[int, int]] = []
        for (x, y), color in grid.get_items():
            if color != selected_color:
                continue

            if (x, y+1) in grid:
                new_squares.append((x, y+1))

            if (x+1, y) in grid:
                new_squares.append((x+1, y))

        for (x, y) in new_squares:
            grid[x, y] = selected_color
