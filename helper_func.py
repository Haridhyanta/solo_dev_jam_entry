from typing import Callable
from pygame import Rect
import pygame as pg


def text_sprite(
        font: pg.font.Font,
        text: str, 
        colour: pg.color.Color,
        *,
        extra_width: int = 0,
        extra_height:int = 0,
        line_colors: dict[int, pg.Color]|None=None,
        line_fonts: dict[int, pg.font.Font]|None=None,
        center_text: bool=False
    ) -> pg.surface.Surface:

    if '\n' not in text:
        if line_fonts is not None and 0 in line_fonts.keys():
            return line_fonts[0].render(text, True, colour)
        return font.render(text, True, colour)

    splited_text = text.split('\n')
    sprites: list[pg.surface.Surface] = []
    biggest_width = 0

    for i, one_line_of_text in enumerate(splited_text):
        current_font: pg.font.Font = font
        if line_fonts is not None:
            current_font = line_fonts.get(i, font)
        sprite = current_font.render(one_line_of_text, True, colour)
        if line_colors is not None:
            if i in line_colors.keys():
                sprite = font.render(one_line_of_text, True, line_colors[i])
        sprites.append(sprite)
        biggest_width = max(sprite.get_width(), biggest_width)
    
    current_height: int = 0
    sprite_heights: list[int] = [x.get_height() for x in sprites]
    final_surface = pg.Surface((biggest_width+extra_width, sum(sprite_heights)+extra_height*len(sprites)), pg.SRCALPHA)
    
    for i, sprite in enumerate(sprites):
        x = 0
        if center_text:
            x = (biggest_width-sprite.get_width())/2
        final_surface.blit(sprite, (x, current_height + extra_height*i))
        current_height += sprite_heights[i]
    
    return final_surface.convert_alpha()

def text_wrap_mono(
        mono_font: pg.font.Font,
        text: str,
        max_width: int,
        colour: pg.color.Color,
        *,
        extra_height:int = 0,
        line_colors: dict[int, pg.Color]|None=None,
        line_mono_fonts: dict[int, pg.font.Font]|None=None,
        center_text: bool=False
    ) -> pg.surface.Surface:
    guess_width: int = mono_font.render('a', True, (0, 0, 0)).get_width()
    if line_mono_fonts is not None:
        guess_width = line_mono_fonts.get(0, mono_font).render('a', True, (0, 0, 0)).get_width()
    current_line_width: int = 0
    old_line_no: int = 0
    new_line_no: int = 0
    final_text: str = ''
    final_line_colors: dict[int, pg.Color] = {}
    final_line_fonts: dict[int, pg.font.Font] = {}
    line_has_multiple_words: bool = False

    current_word_len: int = 0
    current_word_width: int = 0
    if line_mono_fonts is not None and old_line_no in line_mono_fonts.keys():
        final_line_fonts[new_line_no] = line_mono_fonts[old_line_no]

    if line_colors is not None and old_line_no in line_colors.keys():
        final_line_colors[new_line_no] = line_colors[old_line_no]

    for ch in text:
        if ch == '\n':
            final_text = final_text + '\n'
            current_line_width = 0
            current_word_len = 0
            old_line_no += 1
            new_line_no += 1
            line_has_multiple_words = False

            if line_mono_fonts is not None:
                line_font = mono_font
                if old_line_no in line_mono_fonts.keys():
                    line_font = line_mono_fonts[old_line_no]
                    final_line_fonts[new_line_no] = line_font
                guess_width = line_font.render('a', True, (0, 0, 0)).get_width()

            if line_colors is not None and old_line_no in line_colors.keys():
                final_line_colors[new_line_no] = line_colors[old_line_no]

            continue

        current_line_width += guess_width
        current_word_width += guess_width

        is_space = ch.isspace()
        if not is_space:
            current_word_len += 1
        else:
            line_has_multiple_words = True
            current_word_len = 0
            current_word_width = 0
        
        if current_line_width > max_width and not is_space:
            if not line_has_multiple_words:
                final_text = final_text + '\n' + ch
            else:
                i = current_word_len
                if i > 0:
                    final_text = final_text + ch
                    final_text = final_text[:-i] + '\n' + final_text[-i:]
                else:
                    final_text = final_text + '\n'
                    final_text = final_text + ch
            new_line_no += 1
            current_line_width = current_word_width

            if line_mono_fonts is not None and old_line_no in line_mono_fonts.keys():
                final_line_fonts[new_line_no] = line_mono_fonts[old_line_no]

            if line_colors is not None and old_line_no in line_colors.keys():
                final_line_colors[new_line_no] = line_colors[old_line_no]
            continue
    
        final_text = final_text + ch

    return text_sprite(
        mono_font,
        final_text,
        colour,
        extra_height=extra_height,
        line_colors=final_line_colors,
        line_fonts=final_line_fonts,
        center_text=center_text,
    )
