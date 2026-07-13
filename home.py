import asyncio

from game_data import GameData
import pygame as pg
from scenes import Scene


async def home() -> Scene:
    game_data: GameData = GameData()

    screen: pg.surface.Surface = game_data.screen
    WIND_X, WIND_Y = game_data.WIND_X, game_data.WIND_Y
    bg_color: tuple[int, int, int] = game_data.bg_color

    bg_img: pg.surface.Surface = game_data.homepage_img

    audio_on_img = game_data.audio_on_img
    audio_off_img = game_data.audio_off_img
    audio_rect = audio_on_img.get_rect()

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
                if audio_rect.collidepoint(event.pos):
                    game_data.music_is_paused = not game_data.music_is_paused
                    if game_data.music_is_paused:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                    continue

                return Scene.LEVEL
            
            if event.type == pg.KEYDOWN:
                return Scene.LEVEL
            
        screen.blit(bg_img, (0, 0))

        pg.draw.rect(
            screen,
            pg.Color("White"),
                audio_rect.inflate(20, 20),
            10
        )
        screen.blit(audio_off_img if game_data.music_is_paused else audio_on_img, audio_rect)

        pg.display.update()
        await asyncio.sleep(0)