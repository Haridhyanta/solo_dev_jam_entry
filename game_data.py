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

        WIND_X, WIND_Y = 2100, 900
        self.screen: pg.surface.Surface = pg.display.set_mode((WIND_X, WIND_Y), flags=pg.SRCALPHA)
        self.WIND_X, self.WIND_Y = self.screen.get_size()

        self.clock: pg.time.Clock = pg.time.Clock()
        self.max_fps: float = 0

        self.bg_color: tuple[int, int, int] = 0, 0, 0

        self.level_no: int = 1

        self.grey_out_color: pg.Color = pg.Color(50, 50, 50, 50)

        self.normal_font_path = r'./Roboto_Mono/static/RobotoMono-Regular.ttf'
        self.normal_font = pg.font.Font(self.normal_font_path, 28)
        self.small_font = pg.font.Font(self.normal_font_path, 12)
        self.large_font = pg.font.Font(self.normal_font_path, 64)
        self.ui_large_font = pg.font.Font(self.normal_font_path, 200)
        self.bold_font_path = r'./Roboto_Mono/static/RobotoMono-SemiBold.ttf'
        self.bold_font = pg.font.Font(self.bold_font_path, 32)

        self.padlock_img: pg.surface.Surface = pg.transform.scale(pg.image.load('./img/padlock.png'), (50, 50))
        self.next_level_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/next_level.png'), 4.0)
        self.pause_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/pause.png'), 4.0)
        self.unpause_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/unpause.png'), 4.0)
        self.step_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/step.png'), 4.0)

        self.text_color: pg.Color = pg.Color(0, 0, 0)
        self.text_outline_color: pg.Color = pg.Color("WHITE")
