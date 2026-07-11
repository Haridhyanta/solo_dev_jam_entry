from typing import Any, Callable, Coroutine
import asyncio

from scenes import Scene


scenes_to_func: dict[Scene, Callable[[], Coroutine[Any, Any, Scene]]] = {}

async def main():
    current_scene: Scene = Scene.QUIT

    while current_scene != Scene.QUIT:
        current_scene = asyncio.run(scenes_to_func[current_scene]())
    
if __name__ == '__main__':
    asyncio.run(main())
