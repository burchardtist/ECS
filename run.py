from ecs.engine import Engine
from example.systems import RenderableSystem, MovePlayerSystem
from example.utils import setup_map, setup_app, game_loop

if __name__ == '__main__':
    engine = Engine()
    app = setup_app()
    engine.app = app  # todo: add app to the engine
    setup_map(engine)
    engine.add_system(MovePlayerSystem())
    engine.add_system(RenderableSystem())
    game_loop(engine, app)
