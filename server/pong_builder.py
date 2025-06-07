from common.entities.ball import Ball
from common.entities.paddle import Paddle
from server_scene import ServerScene


def build_pong_scene(send_player_events):
    scene = ServerScene(send_player_events)
    paddle_1 = Paddle(0)
    paddle_2 = Paddle(1)

    scene.add_entity(Ball(paddle_1, paddle_2))

    scene.add_entity(paddle_1)
    scene.add_entity(paddle_2)

    return scene
