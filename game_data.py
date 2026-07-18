import os
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

        self.music_is_paused: bool = False

        WIND_X, WIND_Y = 2100, 900
        self.screen: pg.surface.Surface = pg.display.set_mode((WIND_X, WIND_Y), flags=pg.SRCALPHA)
        self.WIND_X, self.WIND_Y = self.screen.get_size()

        self.clock: pg.time.Clock = pg.time.Clock()
        self.max_fps: float = 0

        self.bg_color: tuple[int, int, int] = 0, 0, 0

        self.level_no: int = 1
        self.max_level_no: int = 1
        self.total_no_of_levels: int = 1
        while True:
            if not os.path.exists(f'./levels/level_{self.total_no_of_levels+1}.json'):
                break
            self.total_no_of_levels += 1
            
        self.grey_out_color: pg.Color = pg.Color(50, 50, 50, 50)

        self.normal_font_path = r'./Roboto_Mono/static/RobotoMono-Regular.ttf'
        self.normal_font = pg.font.Font(self.normal_font_path, 28)
        self.small_font = pg.font.Font(self.normal_font_path, 12)
        self.large_font = pg.font.Font(self.normal_font_path, 64)
        self.ui_large_font = pg.font.Font(self.normal_font_path, 200)
        self.ui_max_font = pg.font.Font(self.normal_font_path, 300)
        self.bold_font_path = r'./Roboto_Mono/static/RobotoMono-SemiBold.ttf'
        self.bold_font = pg.font.Font(self.bold_font_path, 28)

        self.padlock_img: pg.surface.Surface = pg.transform.scale(pg.image.load('./img/padlock.png'), (50, 50))
        self.next_level_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/next_level.png'), 4.0)
        self.pause_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/pause.png'), 4.0)
        self.unpause_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/unpause.png'), 4.0)
        self.step_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/step.png'), 4.0)
        self.reset_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/reset.png'), 4.0)
        self.home_img: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/home.png'), 3.0)
        self.homepage_img: pg.surface.Surface = pg.image.load('./img/homepage.png')
        self.audio_on_img: pg.surface.Surface = pg.transform.scale(pg.image.load('./img/audio_on.png'), self.home_img.get_size())
        self.audio_off_img: pg.surface.Surface = pg.transform.scale(pg.image.load('./img/audio_off.png'), self.home_img.get_size())
        self.background_img: pg.surface.Surface = pg.image.load('./img/background.png')
        self.tutorial_prompt_1: pg.surface.Surface = pg.transform.scale_by(pg.image.load('./img/tutorial_prompt_1.png'), 2)
        self.tutorial_prompt_2: pg.surface.Surface = pg.image.load('./img/tutorial_prompt_2.png')
        self.tutorial_prompt_3: pg.surface.Surface = pg.image.load('./img/tutorial_prompt_3.png')
        self.tutorial_prompt_4: pg.surface.Surface = pg.image.load('./img/tutorial_prompt_4.png')
        self.tutorial_prompt_5: pg.surface.Surface = pg.image.load('./img/tutorial_prompt_5.png')
        self.right_arrow: pg.surface.Surface = pg.transform.scale2x(pg.image.load('./img/right_arrow.png'))
        self.up_arrow: pg.surface.Surface = pg.transform.rotate(self.right_arrow, 90)
        self.left_arrow: pg.surface.Surface = pg.transform.rotate(self.up_arrow, 90)
        self.down_arrow: pg.surface.Surface = pg.transform.rotate(self.left_arrow, 90)
        self.x_img: pg.surface.Surface = pg.transform.scale2x(pg.image.load('./img/x_icon.png'))

        self.text_color: pg.Color = pg.Color(0, 0, 0)
        self.text_outline_color: pg.Color = pg.Color("WHITE")
