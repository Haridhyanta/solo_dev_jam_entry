from typing import Any, Callable, Coroutine
import asyncio

import pygame as pg
from game import game
from home import home
from level import level
from scenes import Scene
from game_data import GameData
from scenes import Scene
from thanks import thanks

scenes_to_func: dict[Scene, Callable[[], Coroutine[Any, Any, Scene]]] = {
    Scene.HOME: home,
    Scene.GAME: game,
    Scene.LEVEL: level,
    Scene.THANKS: thanks,
}

GameData()

async def main():
    current_scene: Scene = Scene.HOME
    pg.mixer.init(44100, -16, 2, 2620)
    pg.mixer.music.load('./music/alex-morgan-jazz-rainy-night-music-563584.ogg')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(loops=-1)

    while current_scene != Scene.QUIT:
        current_scene = await scenes_to_func[current_scene]()
        await asyncio.sleep(0)

    pg.mixer_music.stop()
    pg.quit()
    
if __name__ == '__main__':
    asyncio.run(main())
