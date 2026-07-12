from typing import Any, Callable, Coroutine
import asyncio

import pygame as pg
from game import game
from home import home
from scenes import Scene
from game_data import GameData
from scenes import Scene

scenes_to_func: dict[Scene, Callable[[], Coroutine[Any, Any, Scene]]] = {
    Scene.HOME: home,
    Scene.GAME: game,
}

GameData()

async def main():
    current_scene: Scene = Scene.GAME

    while current_scene != Scene.QUIT:
        current_scene = await scenes_to_func[current_scene]()
        await asyncio.sleep(0)

    pg.quit()
    
if __name__ == '__main__':
    asyncio.run(main())
