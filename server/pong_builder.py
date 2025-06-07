from common.entities.ball import Ball
from common.entities.paddle import Paddle
from server_scene import ServerScene


def build_pong_scene(send_player_events):
    scene = ServerScene(send_player_events)
    scene.add_entity(Ball())
    scene.add_entity(Paddle(0))
    scene.add_entity(Paddle(1))

    return scene
