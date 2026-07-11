import pathlib

import pygame as pg

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GameData(metaclass=Singleton):
    def __init__(self):
        pg.init()
        pg.font.init()

        WIND_X, WIND_Y = 1600, 900
        self.screen: pg.surface.Surface = pg.display.set_mode((WIND_X, WIND_Y))
        self.WIND_X, self.WIND_Y = WIND_X, WIND_Y

        self.clock: pg.time.Clock = pg.time.Clock()
        self.max_fps: float = 0

        self.bg_color: tuple[int, int, int] = 0, 0, 0

        self.normal_font_path = r'./Roboto/static/Roboto-Medium.ttf'
        self.normal_font = pg.font.Font(self.normal_font_path, 36)
        self.small_font = pg.font.Font(self.normal_font_path, 16)
        self.bold_font_path = r'./Roboto/static/Roboto-Bold.ttf'
        self.bold_font = pg.font.Font(self.bold_font_path, 32)

        self.text_color: pg.Color = pg.Color(0, 0, 0)
        self.text_outline_color: pg.Color = pg.Color("WHITE")
